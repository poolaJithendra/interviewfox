from fastapi import (
    FastAPI,
    WebSocket,
    UploadFile,
    File,
    Form,
    Query,
)
from pydantic import BaseModel

from app.prompts import INTERVIEW_ANSWER_PROMPT
from app.llm_client import generate_answer
from app.rag import chunk_text, build_index, retrieve_context
from app.ws_answer import websocket_answer_handler
from app.ws_audio import websocket_audio_handler
from app.files import extract_text
from app.session_store import (
    create_session,
    set_docs,
    append_transcript,
    clear_transcript,
    get_session,
)

app = FastAPI(title="InterviewFox API")

# ------------------------------------------------------------------
# Models
# ------------------------------------------------------------------
class QuestionRequest(BaseModel):
    question: str
    resume: str
    job_description: str


# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "InterviewFox backend is running"}


# ------------------------------------------------------------------
# Session Management
# ------------------------------------------------------------------
@app.post("/session/create")
def session_create():
    """
    Creates a new interview session.
    """
    return {"session_id": create_session()}


@app.post("/session/upload")
async def session_upload(
    session_id: str = Form(...),
    resume_file: UploadFile | None = File(None),
    jd_file: UploadFile | None = File(None),
):
    """
    Upload resume and JD (PDF/DOCX/TXT).
    Text is extracted and stored in session.
    """
    resume_text = ""
    jd_text = ""

    if resume_file is not None:
        resume_bytes = await resume_file.read()
        resume_text = extract_text(resume_file.filename, resume_bytes)

    if jd_file is not None:
        jd_bytes = await jd_file.read()
        jd_text = extract_text(jd_file.filename, jd_bytes)

    set_docs(session_id, resume_text, jd_text)

    return {
        "session_id": session_id,
        "resume_chars": len(resume_text),
        "jd_chars": len(jd_text),
    }


# ------------------------------------------------------------------
# IC MODE (Interview Capture)
# ------------------------------------------------------------------
@app.post("/session/ic/start")
def ic_start(session_id: str):
    """
    Clears transcript buffer and starts IC mode.
    """
    clear_transcript(session_id)
    return {"session_id": session_id, "ic": "on"}


@app.post("/session/ic/append")
def ic_append(session_id: str, text: str):
    """
    Appends partial STT text to the session transcript.
    """
    append_transcript(session_id, text)
    return {"session_id": session_id, "ok": True}


@app.post("/session/ic/stop")
def ic_stop(session_id: str):
    """
    Stops IC mode and returns the captured interviewer question.
    """
    session = get_session(session_id)
    question = (session.get("transcript") or "").strip()
    return {"session_id": session_id, "question": question}


# ------------------------------------------------------------------
# REST Answer Endpoint (for manual testing / fallback)
# ------------------------------------------------------------------
@app.post("/answer")
def generate_interview_answer(req: QuestionRequest):
    combined_text = req.resume + "\n" + req.job_description

    chunks = chunk_text(combined_text)
    index, stored_chunks = build_index(chunks)
    context = retrieve_context(req.question, index, stored_chunks)

    prompt = INTERVIEW_ANSWER_PROMPT.format(
        question=req.question,
        context=context,
    )

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "context_used": context,
    }


# ------------------------------------------------------------------
# WebSocket: Streaming Answers (Typing Effect)
# ------------------------------------------------------------------
@app.websocket("/ws/answer")
async def websocket_answer(websocket: WebSocket):
    """
    Streams AI answers token-by-token.
    Session-based resume & JD are used.
    """
    await websocket_answer_handler(websocket)


# ------------------------------------------------------------------
# WebSocket: Audio Input (IC Mode – Whisper, dormant)
# ------------------------------------------------------------------
@app.websocket("/ws/audio")
async def websocket_audio(
    websocket: WebSocket,
    session_id: str = Query(...),
):
    """
    Receives mic audio chunks and appends STT output
    to the session transcript.

    NOTE:
    - Used only during local testing
    - Safe to keep inactive
    """
    await websocket_audio_handler(websocket, session_id)
