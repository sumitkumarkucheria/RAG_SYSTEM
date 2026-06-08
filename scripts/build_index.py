from sentence_transformers import SentenceTransformer
import pdfplumber
import faiss
import numpy as np
import os
import pickle

DOC_FOLDER = r"D:\AI_SERVER\documents"
VECTOR_DB = r"D:\AI_SERVER\vector_db"


def read_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        print(f"Pages: {len(pdf.pages)}")

        for i, page in enumerate(pdf.pages):

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def create_chunks(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())

        start += (chunk_size - overlap)

    return chunks


print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = []

print("\nReading documents...\n")

for filename in os.listdir(DOC_FOLDER):

    path = os.path.join(DOC_FOLDER, filename)

    text = ""

    if filename.lower().endswith(".txt"):

        print(f"Reading TXT: {filename}")

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    elif filename.lower().endswith(".pdf"):

        print(f"\nReading PDF: {filename}")

        text = read_pdf(path)

    else:
        continue

    file_chunks = create_chunks(
        text,
        chunk_size=500,
        overlap=100
    )

    print(f"Chunks created: {len(file_chunks)}")

    for chunk in file_chunks:

        chunks.append({
            "source": filename,
            "text": chunk
        })

print(f"\nTotal chunks: {len(chunks)}")

texts = [c["text"] for c in chunks]

print("\nCreating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(
        embeddings,
        dtype=np.float32
    )
)

os.makedirs(VECTOR_DB, exist_ok=True)

print("\nSaving FAISS index...")

faiss.write_index(
    index,
    os.path.join(VECTOR_DB, "index.faiss")
)

print("Saving chunks...")

with open(
    os.path.join(VECTOR_DB, "chunks.pkl"),
    "wb"
) as f:

    pickle.dump(chunks, f)

print(f"\nIndexed {len(chunks)} chunks successfully.")
