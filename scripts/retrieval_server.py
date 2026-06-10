from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from fastapi import Request
from fastapi.responses import HTMLResponse
import requests
from pydantic import BaseModel

THRESHOLD = 1.20
app = FastAPI()
WORKERS = [
    "192.168.1.164",
    "192.168.1.171",
    "192.168.1.180",
    "192.168.1.225"
]

worker_index = 0

class QuestionRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def home():

    with open(
        r"D:\AI_SERVER\templates\index.html",
        encoding="utf-8"
    ) as f:

        return f.read()

def get_next_worker():

    global worker_index

    attempts = len(WORKERS)

    for _ in range(attempts):

        worker = WORKERS[worker_index]

        worker_index = (
            worker_index + 1
        ) % len(WORKERS)

        try:

            r = requests.get(
                f"http://{worker}:11434",
                timeout=2
            )

            if r.status_code == 200:
                print(f"Using worker: {worker}")
                return worker

        except:
            print(f"Worker unavailable: {worker}")

    return None



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
@app.post("/ask")
def ask(data: QuestionRequest):

    query = data.question

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding, dtype=np.float32),
        5
    )

    best_distance = float(distances[0][0])

    if best_distance > THRESHOLD:

        return {
            "answer":
            "Information not found in knowledge base.",

            "sources": [],

            "best_distance":
            best_distance
        }

    context = ""

    sources = []

    for idx in indices[0]:

        chunk = chunks[idx]

        context += chunk["text"] + "\n\n"

        if chunk["source"] not in sources:
            sources.append(
                chunk["source"]
            )

    prompt = f"""
You are a CBSE Class 10 Science teacher.

Answer ONLY from the provided context.

Do not use outside knowledge.

If the answer is not directly present in the context,
reply exactly:

Information not found in knowledge base.

Context:

{context}

Question:

{query}
"""

    worker = get_next_worker()

    if worker is None:

        return {
            "answer":
            "No workers available.",

            "sources": [],

            "best_distance":
            best_distance
        }

    response = requests.post(
        f"http://{worker}:11434/api/generate",

        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False
        },

        timeout=120
    )

    answer = response.json()["response"]

    return {
        "answer": answer,
        "sources": sources,
        "best_distance": best_distance,
        "worker": worker
    }
