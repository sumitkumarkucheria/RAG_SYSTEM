from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

THRESHOLD = 1.20
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

    best_distance = float(distances[0][0])

    # Knowledge boundary
    if best_distance > THRESHOLD:

        return {
            "found": False,
            "best_distance": best_distance,
            "message": "Information not found in knowledge base."
        }

    results = []

    for rank, idx in enumerate(indices[0]):

        results.append({
            "source": chunks[idx]["source"],
            "text": chunks[idx]["text"],
            "distance": float(distances[0][rank])
        })

    return {
        "found": True,
        "best_distance": best_distance,
        "query": query,
        "results": results
    }
