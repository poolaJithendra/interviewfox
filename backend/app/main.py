from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from app.prompts import INTERVIEW_ANSWER_PROMPT
from app.llm_client import generate_answer
from app.rag import chunk_text, build_index, retrieve_context
from app.ws_answer import websocket_answer_handler

app = FastAPI(title="InterviewFox API")


# -------------------------
# Data Models
# -------------------------
class QuestionRequest(BaseModel):
    question: str
    resume: str
    job_description: str


# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {"status": "InterviewFox backend is running"}


# -------------------------
# REST Answer Endpoint
# -------------------------
@app.post("/answer")
def generate_interview_answer(req: QuestionRequest):
    # Combine resume + JD
    combined_text = req.resume + "\n" + req.job_description

    # Build RAG index
    chunks = chunk_text(combined_text)
    index, stored_chunks = build_index(chunks)

    # Retrieve relevant context
    context = retrieve_context(req.question, index, stored_chunks)

    # Build prompt
    prompt = INTERVIEW_ANSWER_PROMPT.format(
        question=req.question,
        context=context
    )

    # Generate answer
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "context_used": context
    }


# -------------------------
# WebSocket Answer Endpoint
# -------------------------
@app.websocket("/ws/answer")
async def websocket_answer(websocket: WebSocket):
    await websocket_answer_handler(websocket)
