from fastapi import FastAPI
from pydantic import BaseModel
from app.prompts import INTERVIEW_ANSWER_PROMPT

app = FastAPI(title="InterviewFox API")


class QuestionRequest(BaseModel):
    question: str
    resume: str
    job_description: str


@app.get("/health")
def health():
    return {"status": "InterviewFox backend is running"}


@app.post("/answer")
def generate_answer(req: QuestionRequest):
    prompt = INTERVIEW_ANSWER_PROMPT.format(
        question=req.question,
        resume=req.resume,
        job_description=req.job_description,
    )

    # Placeholder – LLM call will be added next
    return {
        "prompt_used": prompt,
        "message": "LLM integration coming next"
    }
