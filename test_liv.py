import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"   # Change to 3B if too slow

print(f"Testing model: {MODEL_NAME}")

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

payload = {
    "model": MODEL_NAME,
    "messages": [
        {"role": "system", "content": "You are Liv from Punishing: Gray Raven. You are gentle, shy, and caring."},
        {"role": "user", "content": "Hello Liv, how are you today?"}
    ],
    "max_tokens": 200,
    "temperature": 0.75
}

response = requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
    headers=headers,
    json=payload
)

if response.status_code == 200:
    result = response.json()
    print("\n✅ Model Response:")
    if isinstance(result, list):
        print(result[0].get("generated_text", "No text"))
    else:
        print(result.get("choices", [{}])[0].get("message", {}).get("content", "No content"))
else:
    print(f"❌ Error {response.status_code}: {response.text}")
