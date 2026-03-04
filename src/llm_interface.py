import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-coder"


def ask_llm(prompt: str) -> str:

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        return "error contacting ollama"

    data = response.json()

    return data["response"]