import requests
import os

GROQ_API_KEY =os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_ai(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(API_URL, headers=headers, json=payload)
    print(r.text)  

    return r.json()["choices"][0]["message"]["content"]