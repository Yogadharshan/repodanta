import requests # type: ignore
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

def ask_llm(prompt: str) -> str:
    try:
        full_response = ""
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": True, # TODO: handle streaming response
            "options": {
                "num_predict": 1024,
                "temperature": 0.3
            }
        }
        
        print("\nanswer\n")
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
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