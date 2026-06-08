import requests

question = input("Question: ")

# STEP 1: Retrieval

retrieval = requests.get(
    "http://localhost:8000/search",
    params={
        "query": question
    }
)

results = retrieval.json()["results"]

context = "\n\n".join(
    item["text"] for item in results
)

# STEP 2: Prompt

prompt = f"""
You must answer ONLY from the provided context.

If the answer is not present in the context, reply:

Information not found in knowledge base.

CONTEXT:

{context}

QUESTION:

{question}
"""

# STEP 3: Worker

response = requests.post(
    "http://192.168.1.164:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    },
    timeout=120
)

print("\nANSWER:\n")
print(response.json()["response"])
