import pyaudio
import pyautogui
import sounddevice as sd
import soundfile as sf
import sys
import threading
from pynput import keyboard
import time
from audio import record_audio
from cleanup import clean_text
from transcription import transcribe

FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
key_held = False

config_options = {
    'temperature': 0.1,
    'num_ctx': 4096,
    'top_p': 0.9
}

recording_event = threading.Event()

class SoundPlayer:
    def __init__(self):
        self.start_sound, self.start_rate = sf.read("sound_effects/start.wav")
        self.stop_sound, self.stop_rate = sf.read("sound_effects/stop.wav")

    def play(self, start: bool):
        sound, rate = (
            (self.start_sound, self.start_rate)
            if start
            else (self.stop_sound, self.stop_rate)
        )
        sd.play(sound, rate)

def full(p):
    audio_int16 = record_audio(RATE, CHANNELS, FORMAT, FRAMES_PER_BUFFER, p, recording_event=recording_event)
    if audio_int16.size == 0:
        print("No audio recorded. Exiting.")
        return
    
    start_time_transcription = time.perf_counter()
    text = transcribe(audio_int16)
    end_time_transcription = time.perf_counter()
    print(f"elapsed (transcription): {end_time_transcription-start_time_transcription}")
    start_time_cleanup = time.perf_counter()
    print("Raw text: " + text)
    text = clean_text(text, config_options)
    end_time_cleanup = time.perf_counter()
    print(f"elapsed (cleanup): {end_time_cleanup-start_time_cleanup}")
    print(f"elapsed (total): {end_time_cleanup-start_time_transcription}")
    print(text)
    output_text = text.replace("Output:", "")
    try:
        pyautogui.write(output_text)
    except pyautogui.FailSafeException:
        print("Execution stopped: Fail-safe triggered by moving mouse to a corner.")
    except TypeError:
        print(f"Type error: Cannot write {type(output_text)}. Convert it to a string first.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def on_press(key, p, sound_player):
    global key_held
    try:
        if key == keyboard.Key.alt_l:
            sound_player.play(True)
            if not key_held:
                key_held = True
                recording_event.set()
                action_thread = threading.Thread(target=full, args=(p,), daemon=True)
                action_thread.start()
        elif key.char == 'q':
            return False
    except AttributeError:
        return

def on_release(key, sound_player):
    global key_held
    try:
        if key == keyboard.Key.alt_l:
            sound_player.play(False)
            key_held = False
            recording_event.clear()
    except AttributeError:
        return

def main():

    p = None
    sound_player = SoundPlayer()

    try:
        p = pyaudio.PyAudio()
        with keyboard.Listener(
            on_press=lambda key: on_press(key, p, sound_player),
            on_release=lambda key: on_release(key, sound_player)
        ) as listener:
            print("Waiting for left alt/option key press")
            listener.join()
    except Exception as e:
        print(f"Failed to initialize PyAudio: {e}")
        return
    finally:
        if p is not None:
            p.terminate()

if __name__ == '__main__':
    main()