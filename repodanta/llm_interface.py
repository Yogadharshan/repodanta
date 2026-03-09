import requests # type: ignore


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def ask_llm(prompt: str) -> str:
    try:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=120)

        response.raise_for_status()

        data = response.json()
        return data.get("response", "")

    except Exception as e:
        return f"LLM error: {e}"