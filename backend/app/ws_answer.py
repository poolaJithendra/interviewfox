from fastapi import WebSocket

from app.prompts import INTERVIEW_ANSWER_PROMPT
from app.rag import chunk_text, build_index, retrieve_context
from app.llm_client import stream_answer
from app.session_store import get_session


async def websocket_answer_handler(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_json()

        session_id = data.get("session_id")
        question = (data.get("question") or "").strip()

        if not session_id:
            await websocket.send_json({
                "type": "error",
                "message": "session_id is required"
            })
            return

        if not question:
            await websocket.send_json({
                "type": "error",
                "message": "Question is empty"
            })
            return

        # 🔹 Load resume & JD from session
        session = get_session(session_id)
        resume = session.get("resume", "")
        job_description = session.get("jd", "")

        combined_text = resume + "\n" + job_description

        # 🔹 Build RAG context
        chunks = chunk_text(combined_text)
        index, stored_chunks = build_index(chunks)
        context = retrieve_context(question, index, stored_chunks)

        prompt = INTERVIEW_ANSWER_PROMPT.format(
            question=question,
            context=context
        )

        # Notify start
        await websocket.send_json({
            "type": "start",
            "context_used": context
        })

        # 🔹 Stream answer token-by-token
        full_answer = []
        for chunk in stream_answer(prompt):
            full_answer.append(chunk)
            await websocket.send_json({
                "type": "delta",
                "content": chunk
            })

        # Final message
        await websocket.send_json({
            "type": "done",
            "content": "".join(full_answer)
        })

    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()
