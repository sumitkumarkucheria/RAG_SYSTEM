import requests

question = input("Question: ")

response = requests.post(
    "http://localhost:8000/ask",
    json={
        "question": question
    }
)

data = response.json()

print("\nANSWER:\n")
print(data["answer"])

print("\nSOURCE(S):")

for source in data["sources"]:
    print("-", source)

print("\nBEST DISTANCE:")
print(data["best_distance"])

print("\nWORKER:")
print(data["worker"])
