# test_api.py
import requests

BASE_URL = "http://localhost:8000"

# 1. Status check
res = requests.get(f"{BASE_URL}/")
print("Status Check:", res.json())

# 2. Upload sample documents
sample_texts = {
    "texts": [
        "Paris is the capital of France. It is known for the Eiffel Tower.",
        "Berlin is the capital of Germany. It has a rich history."
    ]
}
res = requests.post(f"{BASE_URL}/upload", json=sample_texts)
print("Upload Response:", res.json())

# 3. Generate an answer
question = {
    "new_message": {
        "role": "user",
        "content": "What is the capital of France?"
    }
}
res = requests.post(f"{BASE_URL}/generate", json=question)
print("Generated Response:", res.json())
