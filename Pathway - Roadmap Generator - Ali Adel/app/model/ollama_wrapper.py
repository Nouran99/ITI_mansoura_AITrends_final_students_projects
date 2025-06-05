import requests
import os

class OllamaLLM:
    def __init__(self, model: str = os.getenv('MODEL_NAME')):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
            "num_predict": max_tokens
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json()["response"].strip()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to contact Ollama: {e}")
            return ""
        except KeyError:
            print("[ERROR] Unexpected response format from Ollama.")
            return ""
