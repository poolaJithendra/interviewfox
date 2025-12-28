import os
from typing import Iterator
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def generate_answer(prompt: str) -> str:
    """Non-streaming answer (REST endpoint)."""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful interview assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        max_tokens=350,
    )
    return response.choices[0].message.content.strip()


def stream_answer(prompt: str) -> Iterator[str]:
    """Streaming answer chunks (WebSocket typing effect)."""
    stream = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful interview assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        max_tokens=350,
        stream=True,
    )

    for event in stream:
        delta = event.choices[0].delta
        if delta and delta.content:
            yield delta.content
