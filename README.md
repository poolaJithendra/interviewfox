Perfect. Below is a **clean, professional, copy-paste-ready `README.md`** for **InterviewFox** that matches your current architecture and GitHub-only state.

You can **replace your README بالكامل** with this.

---

# 🦊 InterviewFox

**InterviewFox** is a real-time AI interview copilot that helps candidates answer interview questions using their **resume**, **job description**, and **live interviewer questions**.

It is designed as a **candidate-controlled**, **privacy-safe**, and **low-latency** interview assistant.

---

## 🚀 What InterviewFox Does

* Lets candidates **upload resume & job description** (PDF / DOCX)
* Captures **interviewer questions in real time** using IC (Interview Capture) mode
* Uses **RAG (Retrieval Augmented Generation)** for personalized answers
* Streams AI-generated answers **word-by-word (typing effect)**
* Works **locally for testing** (no cloud required initially)

---

## 🧠 Key Concepts

### IC Mode (Interview Capture)

InterviewFox does **not listen continuously**.

The candidate controls capture using **IC ON / IC OFF**:

* IC ON → mic listens to interviewer
* IC OFF → captured question is finalized
* Answer generation starts immediately

This avoids:

* Speaker confusion
* Ethical/legal issues
* Unnecessary background listening

---

## 🧱 Architecture Overview

```
Chrome Extension
 ├── Resume / JD Upload
 ├── IC ON / OFF (Mic Control)
 ├── Live Answer Display (Typing Effect)
 │
FastAPI Backend (Local / Future Cloud)
 ├── Session Management
 ├── Resume & JD Parsing
 ├── RAG (FAISS + Embeddings)
 ├── Whisper STT (Local, Testing)
 ├── LLM Answer Generation
 └── WebSocket Streaming
```

---

## 🗂️ Project Structure

```
interviewfox/
├── backend/
│   ├── app/
│   │   ├── main.py            # API entrypoint
│   │   ├── ws_answer.py       # Streaming answers (WebSocket)
│   │   ├── ws_audio.py        # Mic audio input (IC mode)
│   │   ├── stt_whisper.py     # Local Whisper STT (testing)
│   │   ├── rag.py             # Resume/JD RAG engine
│   │   ├── llm_client.py      # LLM integration
│   │   ├── files.py           # PDF/DOCX text extraction
│   │   └── session_store.py   # In-memory session store
│   └── requirements.txt
│
├── extension/
│   ├── popup.html             # Chrome extension UI
│   └── popup.js               # IC logic + WebSockets
│
└── README.md
```

---

## 📄 Resume & JD Support

Supported formats:

* ✅ PDF
* ✅ DOCX
* ✅ TXT (fallback)

Files are:

* Parsed on upload
* Stored per session
* Used automatically for RAG (no repeated uploads)

---

## 🔊 Audio & STT (Testing Mode)

* Uses **local Whisper (faster-whisper)**
* No cloud STT required for testing
* Mic access is **explicit and user-controlled**
* Audio pipeline is **dormant until backend is run locally**

> ⚠️ Live mic testing requires running the backend locally
> GitHub alone cannot access microphone or run WebSockets

---

## 🔐 Security & Privacy

* No API keys committed to GitHub
* `.env.example` contains placeholders only
* Resume/JD data stored **in-memory (MVP)**
* IC mode prevents continuous listening

---

## 🧪 Current Status

* ✅ Backend architecture complete
* ✅ Chrome extension UI complete
* ✅ IC mode implemented
* ✅ RAG + streaming answers implemented
* ⏳ Local testing (Whisper) pending
* ⏳ Cloud deployment optional (future)

---

## 🛣️ Roadmap

* [ ] Hotkey-based IC control
* [ ] Better question boundary detection
* [ ] Session persistence (Redis / DB)
* [ ] Cloud STT (Deepgram / Azure Speech)
* [ ] Pricing & usage limits
* [ ] Production deployment

---

## 🧠 One-Line Description (for demos)

> **InterviewFox is a real-time AI interview copilot that captures interviewer questions on demand and streams personalized answers using your resume and job description.**
