import numpy as np
import faiss
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chunk_text(text: str, chunk_size: int = 500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks


def embed_texts(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    embeddings = [e.embedding for e in response.data]
    return np.array(embeddings).astype("float32")


def build_index(chunks: list[str]):
    embeddings = embed_texts(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, chunks


def retrieve_context(question: str, index, chunks, top_k: int = 3) -> str:
    q_embedding = embed_texts([question])
    distances, indices = index.search(q_embedding, top_k)
    selected_chunks = [chunks[i] for i in indices[0]]
    return "\n".join(selected_chunks)
