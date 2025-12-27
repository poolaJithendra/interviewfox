"""
WebSocket Audio Handler (IC Mode)

Receives audio chunks from browser mic
Appends transcribed text into session buffer

NOTE:
- Used only during local testing
- Safe to keep unused in production
"""

from fastapi import WebSocket
from app.session_store import append_transcript
from app.stt_whisper import transcribe_wav_bytes


async def websocket_audio_handler(websocket: WebSocket, session_id: str):
    await websocket.accept()

    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            text = transcribe_wav_bytes(audio_bytes)
            if text:
                append_transcript(session_id, text)
    except Exception:
        pass
    finally:
        await websocket.close()
