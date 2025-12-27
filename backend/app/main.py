from fastapi import FastAPI

app = FastAPI(title="InterviewFox API")

@app.get("/health")
def health():
    return {"status": "InterviewFox backend is running"}
