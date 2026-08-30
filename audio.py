import numpy as np

def record_audio(rate: int, channels: int, format, frames_per_buffer: int, p, recording_event):
    try:
        stream = p.open(
            rate=rate,
            channels=channels,
            input=True,
            format=format,
            frames_per_buffer=frames_per_buffer
        )

        frames = []
        while recording_event.is_set():
            data = stream.read(frames_per_buffer)
            frame = np.frombuffer(data, dtype=np.int16)
            frames.append(frame)


        stream.stop_stream()
        stream.close()

        if len(frames) > 1:
            audio_int16 = np.concatenate(frames)
        else:
            audio_int16 = np.array(frames)

        audio_int16 = audio_int16.astype(np.float32) / 32768.0
        return audio_int16
    except Exception as e:
        print(f"An error occurred while recording audio: {e}")
        return np.array([])