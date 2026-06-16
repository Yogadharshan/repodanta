import requests # type: ignore
import json
from repodanta import config

def ask_llm(prompt: str) -> str:
    try:
        full_response = ""
        payload = {
            "model": config.ollama_model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_predict": 1024,
                "temperature": 0.3
            }
        }

        print("\nanswer\n")

        response = requests.post(config.ollama_url, json=payload, timeout=600)
        for chunk in response.iter_lines():
            if chunk:
                data = json.loads(chunk.decode("utf-8"))
                token = data.get("response", "")
                print(token, end="", flush=True)
                full_response += token
                if data.get("done"):
                    break
        print() # for newline after response

        return full_response
    except Exception as e:
        return f"LLM error: {e}"