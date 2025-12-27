from fastapi import FastAPI, WebSocket, UploadFile, File, Form
from pydantic import BaseModel

from app.prompts import INTERVIEW_ANSWER_PROMPT
from app.llm_client import generate_answer
from app.rag import chunk_text, build_index, retrieve_context
from app.ws_answer import websocket_answer_handler

from app.files import extract_text
from app.session_store import (
    create_session, set_docs, append_transcript, clear_transcript, get_session
)

app = FastAPI(title="InterviewFox API")


class QuestionRequest(BaseModel):
    question: str
    resume: str
    job_description: str


@app.get("/health")
def health():
    return {"status": "InterviewFox backend is running"}


# -------------------------
# Session + Docs Upload
# -------------------------
@app.post("/session/create")
def session_create():
    return {"session_id": create_session()}


@app.post("/session/upload")
async def session_upload(
    session_id: str = Form(...),
    resume_file: UploadFile | None = File(None),
    jd_file: UploadFile | None = File(None),
):
    resume_text = ""
    jd_text = ""

    if resume_file is not None:
        resume_bytes = await resume_file.read()
        resume_text = extract_text(resume_file.filename, resume_bytes)

    if jd_file is not None:
        jd_bytes = await jd_file.read()
        jd_text = extract_text(jd_file.filename, jd_bytes)

    set_docs(session_id, resume_text, jd_text)

    return {"session_id": session_id, "resume_chars": len(resume_text), "jd_chars": len(jd_text)}


# -------------------------
# IC Mode: transcript buffer
# -------------------------
@app.post("/session/ic/start")
def ic_start(session_id: str):
    clear_transcript(session_id)
    return {"session_id": session_id, "ic": "on"}


@app.post("/session/ic/append")
def ic_append(session_id: str, text: str):
    append_transcript(session_id, text)
    return {"session_id": session_id, "ok": True}


@app.post("/session/ic/stop")
def ic_stop(session_id: str):
    s = get_session(session_id)
    question = (s.get("transcript") or "").strip()
    return {"session_id": session_id, "question": question}


# -------------------------
# REST Answer Endpoint (still useful)
# -------------------------
@app.post("/answer")
def generate_interview_answer(req: QuestionRequest):
    combined_text = req.resume + "\n" + req.job_description
    chunks = chunk_text(combined_text)
    index, stored_chunks = build_index(chunks)
    context = retrieve_context(req.question, index, stored_chunks)

    prompt = INTERVIEW_ANSWER_PROMPT.format(question=req.question, context=context)
    answer = generate_answer(prompt)

    return {"answer": answer, "context_used": context}


# -------------------------
# WebSocket Answer Endpoint (streaming)
# -------------------------
@app.websocket("/ws/answer")
async def websocket_answer(websocket: WebSocket):
    await websocket_answer_handler(websocket)
