from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index(
    r"D:\AI_SERVER\vector_db\index.faiss"
)

with open(
    r"D:\AI_SERVER\vector_db\chunks.pkl",
    "rb"
) as f:
    chunks = pickle.load(f)

query = input("Question: ")

query_embedding = model.encode([query])

distances, indices = index.search(
    np.array(query_embedding, dtype=np.float32),
    5
)

print("\nTop Matches:\n")

for rank, idx in enumerate(indices[0], start=1):
    chunk = chunks[idx]

    print(f"{rank}. Source: {chunk['source']}")
    print(chunk["text"])
    print("-" * 50)
