from typing import Dict
from uuid import uuid4

# Simple in-memory store for MVP. Replace with Redis/DB later.
SESSIONS: Dict[str, Dict] = {}

def create_session() -> str:
    sid = str(uuid4())
    SESSIONS[sid] = {"resume": "", "jd": "", "transcript": ""}
    return sid

def set_docs(session_id: str, resume: str, jd: str) -> None:
    SESSIONS.setdefault(session_id, {})
    SESSIONS[session_id]["resume"] = resume or ""
    SESSIONS[session_id]["jd"] = jd or ""

def append_transcript(session_id: str, text: str) -> None:
    SESSIONS.setdefault(session_id, {})
    prev = SESSIONS[session_id].get("transcript", "")
    SESSIONS[session_id]["transcript"] = (prev + " " + (text or "")).strip()

def clear_transcript(session_id: str) -> None:
    if session_id in SESSIONS:
        SESSIONS[session_id]["transcript"] = ""

def get_session(session_id: str) -> Dict:
    return SESSIONS.get(session_id, {})
