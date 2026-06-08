from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

app = FastAPI()

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index(
    r"D:\AI_SERVER\vector_db\index.faiss"
)

print("Loading chunks...")
with open(
    r"D:\AI_SERVER\vector_db\chunks.pkl",
    "rb"
) as f:
    chunks = pickle.load(f)

print("Knowledge server ready.")


@app.get("/search")
def search(query: str, top_k: int = 5):

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding, dtype=np.float32),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append({
            "source": chunks[idx]["source"],
            "text": chunks[idx]["text"]
        })

    return {
        "query": query,
        "results": results
    }