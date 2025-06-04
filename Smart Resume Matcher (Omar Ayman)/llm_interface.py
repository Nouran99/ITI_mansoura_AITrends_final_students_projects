import os
import requests
from dotenv import load_dotenv
import json
from huggingface_hub import InferenceClient
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

def ask_llm(prompt: str) -> str:
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        return "❌ No Hugging Face token found. Please provide one in the app."

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,      # Increased for meaningful output
            "do_sample": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Handle multiple possible return formats
        if isinstance(result, list):
            item = result[0]
            if isinstance(item, dict) and "generated_text" in item:
                return item["generated_text"].strip()
            elif isinstance(item, str):
                return item.strip()
            else:
                return json.dumps(result)
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"].strip()
        else:
            return json.dumps(result)

    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {e}"
    except Exception as e:
        return f"❌ Unhandled error: {e}"