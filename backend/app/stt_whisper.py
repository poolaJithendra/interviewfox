from faster_whisper import WhisperModel
import tempfile

model = WhisperModel("small", compute_type="int8")

def transcribe_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
        f.write(audio_bytes)
        f.flush()

        segments, _ = model.transcribe(f.name)
        return " ".join(seg.text for seg in segments)
