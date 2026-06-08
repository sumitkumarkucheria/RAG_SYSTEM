from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import re
#paragraph chunking file
DOC_FOLDER = r"D:\AI_SERVER\documents"

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = []

for filename in os.listdir(DOC_FOLDER):
    if filename.endswith(".txt"):
        path = os.path.join(DOC_FOLDER, filename)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        paragraphs = re.split(r'\n\s*\n', text)

        for p in paragraphs:
            p = p.strip()

            if len(p) > 50:
                chunks.append({
                    "source": filename,
                    "text": p
                })

texts = [c["text"] for c in chunks]

embeddings = model.encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings, dtype=np.float32))

faiss.write_index(
    index,
    r"D:\AI_SERVER\vector_db\index.faiss"
)

with open(
    r"D:\AI_SERVER\vector_db\chunks.pkl",
    "wb"
) as f:
    pickle.dump(chunks, f)

print(f"Indexed {len(chunks)} chunks")
