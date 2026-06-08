import requests

response = requests.post(
    "http://192.168.1.164:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": "What is Python?",
        "stream": False
    },
    timeout=120
)

print(response.json()["response"])
