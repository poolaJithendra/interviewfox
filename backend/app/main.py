# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import uuid
# import os
# from fastapi import FastAPI, UploadFile, File, Form, Body

# from openai import OpenAI
# from openai import OpenAI


# # -------------------------------------------------
# # Load env + OpenAI client
# # -------------------------------------------------
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # -------------------------------------------------
# # Simple in-memory session store (MVP)
# # -------------------------------------------------
# SESSIONS = {}

# def create_session():
#     session_id = str(uuid.uuid4())
#     SESSIONS[session_id] = {
#         "resume": "",
#         "jd": "",
#         "transcript": "",
#     }
#     return session_id

# def set_docs(session_id, resume, jd):
#     SESSIONS[session_id]["resume"] = resume
#     SESSIONS[session_id]["jd"] = jd

# def clear_transcript(session_id):
#     SESSIONS[session_id]["transcript"] = ""

# def get_session(session_id):
#     return SESSIONS.get(session_id, {})

# # -------------------------------------------------
# # FastAPI init
# # -------------------------------------------------
# app = FastAPI(title="InterviewFox API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------------------------------------
# # Health
# # -------------------------------------------------
# @app.get("/health")
# def health():
#     return {"status": "InterviewFox backend is running"}

# # -------------------------------------------------
# # Session APIs
# # -------------------------------------------------
# @app.post("/session/create")
# def session_create():
#     return {"session_id": create_session()}

# @app.post("/session/upload")
# async def session_upload(
#     session_id: str = Form(...),
#     resume_file: UploadFile | None = File(None),
#     jd_file: UploadFile | None = File(None),
# ):
#     resume_text = ""
#     jd_text = ""

#     if resume_file:
#         resume_text = (await resume_file.read()).decode(errors="ignore")

#     if jd_file:
#         jd_text = (await jd_file.read()).decode(errors="ignore")

#     set_docs(session_id, resume_text, jd_text)

#     return {
#         "session_id": session_id,
#         "resume_chars": len(resume_text),
#         "jd_chars": len(jd_text),
#     }

# # -------------------------------------------------
# # IC MODE (logic only)
# # -------------------------------------------------
# @app.post("/session/ic/start")
# def ic_start(session_id: str):
#     clear_transcript(session_id)
#     return {"ic": "on"}

# @app.post("/session/ic/stop")
# def ic_stop(session_id: str):
#     session = get_session(session_id)
#     return {"question": session.get("transcript", "").strip()}

# # -------------------------------------------------
# # Generate API (OpenAI)
# # -------------------------------------------------
# class GenerateRequest(BaseModel):
#     question: str

# # @app.post("/generate")
# # def generate(payload: GenerateRequest):
# #     question = payload.question.strip()

# #     if not question:
# #         return {"answer": ""}

# #     response = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         messages=[
# #             {
# #                 "role": "system",
# #                 "content": "You are an interview assistant. Answer clearly and professionally."
# #             },
# #             {
# #                 "role": "user",
# #                 "content": question
# #             }
# #         ],
# #         temperature=0.4,
# #         max_tokens=250
# #     )

# #     return {
# #         "answer": response.choices[0].message.content.strip()
# #     }


# @app.post("/generate")
# def generate(data: dict = Body(...)):
#     question = data.get("question", "").strip()
#     if not question:
#         return {"answer": ""}

#     context = ""
#     chunks = SESSIONS.get(data.get("session_id"), {}).get("chunks", [])
#     if chunks:
#         context = retrieve_context(question, chunks)

#     system_prompt = f"""
# You are a senior interview assistant.
# Answer concisely, confidently, and in first person.
# Use the candidate's resume and job description when relevant.
# If context is missing, still answer professionally.
# """

#     user_prompt = f"""
# Question:
# {question}

# Context (resume + JD excerpts):
# {context}
# """

#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ],
#         temperature=0.3,
#         max_tokens=180
#     )

#     return {"answer": response.choices[0].message.content.strip()}

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from dotenv import load_dotenv
from openai import OpenAI
import uuid
import os

# -------------------------------------------------
# Load env + OpenAI client
# -------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------------------------
# In-memory session store (MVP)
# -------------------------------------------------
SESSIONS = {}

def create_session():
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "resume": "",
        "jd": "",
        "transcript": "",
    }
    return session_id

def set_docs(session_id, resume, jd):
    if session_id in SESSIONS:
        SESSIONS[session_id]["resume"] = resume
        SESSIONS[session_id]["jd"] = jd

def clear_transcript(session_id):
    if session_id in SESSIONS:
        SESSIONS[session_id]["transcript"] = ""

def get_session(session_id):
    return SESSIONS.get(session_id, {})

# -------------------------------------------------
# FastAPI init
# -------------------------------------------------
app = FastAPI(title="InterviewFox API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Health
# -------------------------------------------------
@app.get("/health")
def health():
    return {"status": "InterviewFox backend is running"}

# -------------------------------------------------
# Session APIs
# -------------------------------------------------
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

    if resume_file:
        resume_text = (await resume_file.read()).decode(errors="ignore")

    if jd_file:
        jd_text = (await jd_file.read()).decode(errors="ignore")

    set_docs(session_id, resume_text, jd_text)

    return {
        "session_id": session_id,
        "resume_chars": len(resume_text),
        "jd_chars": len(jd_text),
    }

# -------------------------------------------------
# IC MODE (logic only)
# -------------------------------------------------
@app.post("/session/ic/start")
def ic_start(session_id: str):
    clear_transcript(session_id)
    return {"ic": "on"}

@app.post("/session/ic/stop")
def ic_stop(session_id: str):
    session = get_session(session_id)
    return {"question": session.get("transcript", "").strip()}

# -------------------------------------------------
# Generate Answer (OpenAI – WORKING)
# -------------------------------------------------
# @app.post("/generate")
# def generate(data: dict = Body(...)):
#     question = data.get("question", "").strip()
#     session_id = data.get("session_id")

#     if not question:
#         return {"answer": ""}

#     resume = ""
#     jd = ""

#     if session_id and session_id in SESSIONS:
#         resume = SESSIONS[session_id].get("resume", "")
#         jd = SESSIONS[session_id].get("jd", "")

#     context = ""
#     if resume or jd:
#         context = f"""
# Candidate Resume:
# {resume[:2000]}

# Job Description:
# {jd[:2000]}
# """

#     system_prompt = (
#         "You are a senior interview assistant. "
#         "Answer in first person, confidently and concisely. "
#         "Use resume and job description when relevant. "
#         "Avoid fluff."
#     )

#     user_prompt = f"""
# Interview Question:
# {question}

# Context:
# {context}
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ],
#         temperature=0.3,
#         max_tokens=180,
#     )

#     return {
#         "answer": response.choices[0].message.content.strip()
#     }

from pydantic import BaseModel
from fastapi import Body

class GenerateRequest(BaseModel):
    question: str
    session_id: str | None = None

@app.post("/generate")
def generate(payload: GenerateRequest):
    question = payload.question.strip()
    session_id = payload.session_id

    resume = ""
    jd = ""

    if session_id and session_id in SESSIONS:
        resume = SESSIONS[session_id].get("resume", "")
        jd = SESSIONS[session_id].get("jd", "")

    context = ""
    if resume or jd:
        context = f"""
Candidate Resume:
{resume[:2000]}

Job Description:
{jd[:2000]}
"""

    system_prompt = (
        "You are a senior interview assistant. "
        "Answer in first person, confidently and concisely. "
        "Use resume and job description when relevant. "
        "Avoid fluff."
    )

    user_prompt = f"""
Interview Question:
{question}

Context:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=180,
    )

    return {"answer": response.choices[0].message.content.strip()}
