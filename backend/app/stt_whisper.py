"""
Local Whisper STT (testing only)

NOTE:
- This file is NOT executed in GitHub
- It is for future local testing only
- No cloud, no API calls here
"""

from faster_whisper import WhisperModel
import tempfile
import os

# Small model for fast local testing
model = WhisperModel("small", device="cpu", compute_type="int8")

def transcribe_wav_bytes(audio_bytes: bytes) -> str:
    """
    Convert WAV audio bytes to text using local Whisper
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name

    segments, _ = model.transcribe(tmp_path)
    os.remove(tmp_path)

    return " ".join(seg.text for seg in segments).strip()
