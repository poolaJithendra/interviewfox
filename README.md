# 🦊 InterviewFox

**InterviewFox** is an AI-powered interview assistance tool that helps candidates generate **high-quality, context-aware answers in real time** during interviews — while remaining **discreet and invisible** during screen sharing.

It combines a **FastAPI backend**, **OpenAI models**, and a **Chrome extension UI** designed specifically for live interview scenarios.

---

## 🚀 What Is Implemented (Current State)

### 1. Backend (FastAPI)

* ✅ Health check API (`/health`)
* ✅ Session management

  * Create interview session
  * Upload Resume & Job Description
* ✅ Secure OpenAI integration (backend-only)
* ✅ Answer generation API (`/generate`)
* ✅ CORS enabled for Chrome extension
* ✅ In-memory session store (MVP)

### 2. AI Capabilities

* Uses **gpt-4o-mini** for:

  * Fast response time
  * Low latency (< ~2s)
* Context-aware answers using:

  * Uploaded resume
  * Uploaded job description
* Prompt optimized for:

  * First-person answers
  * Interview-style clarity
  * Minimal fluff

### 3. Chrome Extension (UI)

* ✅ Popup UI

  * Upload resume & JD
  * Start / stop mic
  * View captured question
  * View AI-generated answer
* ✅ Browser-native speech-to-text
* ✅ Extension UI is **not visible** during screen sharing
* ✅ No API keys exposed in frontend

### 4. Security & Git Hygiene

* ✅ `.env` excluded from Git
* ✅ Secrets removed from Git history
* ✅ `.env.example` provided
* ✅ Backend-only AI access

---

## 🧱 Architecture Overview

### High-Level Flow

```
┌─────────────────────────┐
│   Interviewer (Audio)   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Chrome Extension (UI)  │
│  - Mic capture          │
│  - Speech-to-text       │
│  - Resume & JD upload   │
│  - Displays answers     │
└────────────┬────────────┘
             │  HTTP (JSON)
             ▼
┌─────────────────────────┐
│   FastAPI Backend       │
│  - Session management   │
│  - Resume/JD storage    │
│  - Prompt construction  │
│  - Security boundary    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     OpenAI API          │
│  - gpt-4o-mini          │
│  - Low-latency answers  │
└─────────────────────────┘
```

---

### Key Architectural Decisions

* **No API keys in extension**

  * All AI calls go through backend
* **In-memory sessions (for MVP)**

  * Keeps latency low
  * Simplifies early iteration
* **Context injection over heavy RAG (for now)**

  * Resume + JD included directly in prompt
  * Faster than embeddings during MVP

---

## 🛠️ How to Run Locally

### Prerequisites

* Python 3.10+
* Chrome browser
* OpenAI API key

---

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Create `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Run server:

```bash
uvicorn app.main:app --reload
```

Access:

* API: `http://127.0.0.1:8000`
* Docs: `http://127.0.0.1:8000/docs`

---

### Chrome Extension Setup

1. Open Chrome
2. Go to `chrome://extensions`
3. Enable **Developer mode**
4. Click **Load unpacked**
5. Select `backend/extension`
6. Pin the extension

---

## 🧪 How to Use InterviewFox

1. **Create Session**

   * Upload resume & job description

2. **Start Mic**

   * Capture interviewer’s question

3. **Generate Answer**

   * AI generates response instantly
   * Uses resume + JD context

> The extension UI is local and **not shared** during screen sharing.

---

## ⚠️ Current Limitations (Known)

* ❌ In-memory sessions (no persistence)
* ❌ No Redis caching yet
* ❌ No embeddings-based RAG
* ❌ System audio capture not supported
* ❌ No authentication or rate limiting

These are **intentional MVP tradeoffs**.

---

## 🧭 Roadmap

### Phase 1 – Stability & Speed (Next)

* 🔲 Redis for session storage
* 🔲 Redis cache for repeated answers
* 🔲 <1.5s consistent response latency
* 🔲 Better error handling & retries

### Phase 2 – Smarter AI (RAG)

* 🔲 Resume & JD embeddings (one-time per session)
* 🔲 Vector search for relevant context
* 🔲 Token-efficient prompt construction
* 🔲 Much higher answer relevance

### Phase 3 – UX & Polish

* 🔲 Streaming answers (typing effect)
* 🔲 Clear “listening / thinking” indicators
* 🔲 UI/UX refinements
* 🔲 Multi-language support

### Phase 4 – Security & Scale

* 🔲 Rate limiting
* 🔲 Abuse detection
* 🔲 Auth (optional)
* 🔲 Dockerized deployment
* 🔲 Cloud hosting (AWS / Azure)

---

## 🎯 Long-Term Vision

InterviewFox aims to be a **real-time AI copilot for interviews** — fast, discreet, and context-aware — without violating interview platform visibility or security.

The architecture is intentionally lightweight now, with a clear path to enterprise-grade scalability.

---

## 📌 Notes

* Project is currently in **MVP / experimental stage**
* Designed for rapid iteration
* Safe to open-source or share

⚠️ IMPORTANT DISCLAIMER – READ FIRST

InterviewFox is an experimental project built strictly for:

Interview preparation

Mock interviews

Personal practice

Real-time rehearsal in controlled environments

🚫 This tool must NOT be used in real interviews, live assessments, or hiring evaluations.
🚫 Using this tool in real interviews may violate company policies, ethical standards, or legal agreements.

The author assumes no responsibility for misuse.
By using this project, you agree to use it only for experimentation and preparation purposes.
