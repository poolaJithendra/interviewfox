from fastapi import WebSocket
from app.prompts import INTERVIEW_ANSWER_PROMPT
from app.llm_client import generate_answer
from app.rag import chunk_text, build_index, retrieve_context


async def websocket_answer_handler(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_json()

        question = data.get("question", "")
        resume = data.get("resume", "")
        job_description = data.get("job_description", "")

        combined_text = resume + "\n" + job_description
        chunks = chunk_text(combined_text)
        index, stored_chunks = build_index(chunks)

        context = retrieve_context(question, index, stored_chunks)

        prompt = INTERVIEW_ANSWER_PROMPT.format(
            question=question,
            context=context
        )

        # For now: full answer (streaming token-by-token comes next)
        answer = generate_answer(prompt)

        await websocket.send_json({
            "type": "answer",
            "content": answer
        })

    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        await websocket.close()
