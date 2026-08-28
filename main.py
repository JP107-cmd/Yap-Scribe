import pyaudio
import pyautogui
import sounddevice as sd
import soundfile as sf
import threading
import numpy as np
from faster_whisper import WhisperModel
from pynput import keyboard
from ollama import chat
import time

FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
model = WhisperModel("base.en", device="auto", compute_type="int8")
start_sound, start_rate = sf.read("sound_effects/start.wav")
stop_sound, stop_rate = sf.read("sound_effects/stop.wav")
is_active = False
key_held = False

config_options = {
    'temperature': 0.1,
    'num_ctx': 4096,
    'top_p': 0.9
}

def play_sound(start):
    if start:
        wave = sd.play(start_sound, start_rate)
    else:
        wave = sd.play(stop_sound, stop_rate)

def clean_text(text: str) -> str:
    cleaned_text = chat(
        model='qwen3:4b-q4_K_M',
        options=config_options,
        think=False,
        messages=[{'role': 'user', 'content': 
            f"""
            ROLE:
            You are a text-cleanup service.
            OBJECTIVE:
            You are to clean up inputted text, removing unnecessary filler words, or any statements followed by a retracting statement, ENSURING THE ORIGINAL MEANING OF THE TEXT IS PRESERVED.
            RULES:
            1. Remove all filler/uncessary words from input such as "like, uh, um, etc.". Note: only remove filler/unnecessary words when they
            serve as conversational filler and do not change the meaning of the text.
            Examples: 
                "I uh think the button should be blue." should become "I think the button should be blue".
                "So we should probably move the database logic into its own file, um, and then import it into the main application." should become
                "We should probably move the database logic into its own file and then import it into the main application."
            2. Add or correct punctuation and capitalization of input so that the output is grammatically correct.
            Examples: 
                "I think we should use the blue button because it looks better" should be "I think we should use the blue button because it looks better."
                "Hey John I finished the project can you take a look at it" should be "Hey John, I finished the project. Can you take a look at it?"
            3. When the input retracts, corrects or replaces a previous statement, remove the retracted text and keep only the corrected text. Note: only treat words that often signify retractions (nevermind, no, actually, wait, sorry) as retractions when the context of the entire input signifies that the speaker wishes to correct themselves, not any time when this terminology is used.
            Examples:
                "I like the colour blue, nevermind I like the colour red." should be "I like the colour red."
                "I like the colour blue, no red." should be "I like the colour red."
                "Let's use the blue button, actually let's use the green button." should be "Let's use the green button."
                "I think we should use blue, no red, actually green." should be "I think we should use green"
                "The website should have a dark blue background with white text, nevermind, let's make the background light gray." should be "Let's make the background light gray.",
                "I think we should use the blue button because, well, actually, after thinking about it, I think green would be better." should be "I think we should use the green button"
                "I think we should launch the website next Friday, no, next Monday, because we still need to finish testing." should be "I think we should launch the website next Monday because we still need to finish testing."
                Alternatively, the use of no and actually may not signify a retraction ("No, I think the blue button looks better." or "Actually, I think the current design looks pretty good.")
            4. Remove any repetitions seen in natural speech.
            5. Never add any information not present in the input.
            6. Never change the meaning of the input.
            7. Do not rewrite or change the input if no issues with the input (criteria for an issue outlined in previous rules) is observed.
            8. If the input is empty, output nothing.
            8. Output only the cleaned text.
            INPUT: {text}
            """
        }]
        )
    print(cleaned_text.message.content + " hello ")
    return cleaned_text.message.content

def record_audio():
    global is_active
    stream = p.open(
        rate=RATE,
        channels=CHANNELS,
        input=True,
        format=FORMAT,
        frames_per_buffer=FRAMES_PER_BUFFER
    )
    frames = []
    while is_active:
        data = stream.read(FRAMES_PER_BUFFER)
        frame = np.frombuffer(data, dtype=np.int16)
        frames.append(frame)


    stream.stop_stream()
    stream.close()

    if len(frames) > 1:
        audio_int16 = np.concatenate(frames)
    else:
        audio_int16 = np.array(frames)

    audio_int16 = audio_int16.astype(np.float32) / 32768.0
    start_time_transcription = time.perf_counter()
    segments, _ = model.transcribe(audio_int16, language="en", beam_size=1)
    text = " ".join(seg.text for seg in segments).strip()
    end_time_transcription = time.perf_counter()
    print(f"elapsed (transcription): {end_time_transcription-start_time_transcription}")
    start_time_cleanup = time.perf_counter()
    print("Raw text: " + text)
    text = clean_text(text)
    end_time_cleanup = time.perf_counter()
    print(f"elapsed (cleanup): {end_time_cleanup-start_time_cleanup}")
    print(f"elapsed (total): {end_time_cleanup-start_time_transcription}")
    print(text)
    output_text = text.replace("Output:", "")
    pyautogui.write(output_text)


def on_press(key):
    global is_active
    global key_held
    try:
        if key == keyboard.Key.alt_l:
            if not key_held:
                play_sound(True)
                is_active = True
                key_held = True
                action_thread = threading.Thread(target=record_audio, daemon=True)
                action_thread.start()

        elif key.char == 'q':
            p.terminate()
            return False
    except AttributeError:
        return

def on_release(key):
    global is_active
    global key_held
    try:
        if key == keyboard.Key.alt_l:
            play_sound(False)
            key_held = False
            is_active = False
    except AttributeError:
        return

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Waiting for left alt/option key press")
    listener.join()