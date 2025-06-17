import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_feedback(user_log):
    prompt = f"""
You are a kind, motivating personal life coach. Based on this user log:

{user_log}

Give motivational feedback and one suggestion to improve tomorrow.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error from Gemini API: {e}"
