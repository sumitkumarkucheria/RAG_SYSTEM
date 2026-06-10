import requests
import json

WORKERS = [
    "192.168.1.164",
    "192.168.1.171",
    "192.168.1.180",
    "192.168.1.225"
]


def get_available_worker():

    for worker in WORKERS:

        try:

            response = requests.get(
                f"http://{worker}:11434",
                timeout=2
            )

            if response.status_code == 200:
                print(f"\nUsing worker: {worker}")
                return worker

        except:
            print(f"\nWorker unavailable: {worker}")

    return None

question = input("Question: ")

# STEP 1: Retrieval

retrieval = requests.get(
    "http://localhost:8000/search",
    params={
        "query": question
    }
)

data = retrieval.json()
best_distance = data["best_distance"]

if not data["found"]:
    print("\nInformation not found in knowledge base.")
    exit()



results = data["results"]

sources = []

for item in results:

    if item["source"] not in sources:
        sources.append(item["source"])

context = "\n\n".join(
    item["text"] for item in results
)

# STEP 2: Prompt

prompt = f"""

CONTEXT:

{context}

QUESTION:

{question}

Explain the context like you are 10 grade CBSE teacher of subject
You must answer ONLY from the provided context.

If the answer is not present in the context, reply:

Information not found in knowledge base.


"""

# STEP 3: Worker

worker = get_available_worker()

if worker is None:

    print(
        "\nNo workers available."
    )

    exit()

response = requests.post(
    f"http://{worker}:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": True
    },
    stream=True,
    timeout=120
)

full_answer = ""

for line in response.iter_lines():

    if line:

        data = json.loads(line)

        token = data.get("response", "")

        print(token, end="", flush=True)

        full_answer += token

print()




print("\nSOURCE(S):")

for source in sources:
    print("-", source)
    
print("\nBEST DISTANCE:")
print(best_distance)