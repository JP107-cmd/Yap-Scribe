from faster_whisper import WhisperModel

model = WhisperModel("small.en", device="auto", compute_type="int8")

def transcribe(audio_int16):
    try:
        segments, _ = model.transcribe(audio_int16, language="en", beam_size=1)
        text = " ".join(seg.text for seg in segments).strip()
        return text
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""