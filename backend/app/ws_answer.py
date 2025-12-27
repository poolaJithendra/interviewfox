from fastapi import WebSocket

from app.prompts import INTERVIEW_ANSWER_PROMPT
from app.rag import chunk_text, build_index, retrieve_context
from app.llm_client import stream_answer


async def websocket_answer_handler(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_json()

        question = (data.get("question") or "").strip()
        resume = data.get("resume") or ""
        job_description = data.get("job_description") or ""

        if not question:
            await websocket.send_json({"type": "error", "message": "Question is required."})
            return

        combined_text = resume + "\n" + job_description
        chunks = chunk_text(combined_text)
        index, stored_chunks = build_index(chunks)
        context = retrieve_context(question, index, stored_chunks)

        prompt = INTERVIEW_ANSWER_PROMPT.format(question=question, context=context)

        # Notify client stream is starting
        await websocket.send_json({"type": "start", "context_used": context})

        # Stream chunks
        full = []
        for chunk in stream_answer(prompt):
            full.append(chunk)
            await websocket.send_json({"type": "delta", "content": chunk})

        # Final message
        await websocket.send_json({"type": "done", "content": "".join(full)})

    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        await websocket.close()
