import os
import groq
from dotenv import load_dotenv

load_dotenv()

try:
    client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    models = client.models.list()
    print("Available models:")
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error: {str(e)}")