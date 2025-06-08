# Config/llm.py

from Config.shared import *
from Config.env import GEMINI_API_KEY

basic_llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0.2,
    provider="google_ai_studio",
    api_key=GEMINI_API_KEY
)

