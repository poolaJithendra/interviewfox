from fastapi import FastAPI
from pydantic import BaseModel
from app.prompts import INTERVIEW_ANSWER_PROMPT
from app.llm_client import generate_answer
from app.rag import chunk_text, build_index, retrieve_context

app = FastAPI(title="InterviewFox API")


class QuestionRequest(BaseModel):
    question: str
    resume: str
    job_description: str


@app.get("/health")
def health():
    return {"status": "InterviewFox backend is running"}


@app.post("/answer")
def generate_interview_answer(req: QuestionRequest):
    combined_text = req.resume + "\n" + req.job_description
    chunks = chunk_text(combined_text)
    index, stored_chunks = build_index(chunks)

    context = retrieve_context(req.question, index, stored_chunks)

    prompt = INTERVIEW_ANSWER_PROMPT.format(
        question=req.question,
        context=context
    )

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "context_used": context
    }
