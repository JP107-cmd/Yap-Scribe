import pyaudio
import threading
import numpy as np
from faster_whisper import WhisperModel
from pynput import keyboard

FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
model = WhisperModel("medium.en", device="cpu", compute_type="int8")

is_active = False
key_held = False

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
    segments, _ = model.transcribe(audio_int16, language="en", beam_size=1)
    text = " ".join(seg.text for seg in segments).strip()
    print(text)

def on_press(key):
    global is_active
    global key_held
    try:
        if key == keyboard.Key.cmd:
            if not key_held:
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
        if key == keyboard.Key.cmd:
            key_held = False
            is_active = False
    except AttributeError:
        return

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Waiting for cmd press")
    listener.join()