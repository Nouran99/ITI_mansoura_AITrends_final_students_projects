# models/huggingface_llm.py
from crewai import BaseLLM
from huggingface_hub import InferenceClient
from typing import Dict, Any, Optional, Union
import os
from dotenv import load_dotenv
import requests

class HuggingFaceLLM(BaseLLM):
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.3", api_token: Optional[str] = None, temperature: float = 0.5, max_new_tokens: int = 1024):
        if api_token is None:
            from dotenv import load_dotenv
            load_dotenv()
            api_token = os.getenv("HF_TOKEN")

        if not api_token:
            raise ValueError("Hugging Face API token is missing.")

        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.params = {
            "temperature": temperature,
            "max_new_tokens": max_new_tokens,
            "return_full_text": False
        }

    def call(self, prompt: Union[str, list], **kwargs) -> str:
        if isinstance(prompt, list):
            prompt = "\n".join(
                item.get("content", str(item)) if isinstance(item, dict) else str(item)
                for item in prompt
            )

        print("🧠 Prompt sent to HF API:\n", prompt[:1000], "\n...")
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt, **self.params})
        response.raise_for_status()
        return response.json()[0]["generated_text"]



