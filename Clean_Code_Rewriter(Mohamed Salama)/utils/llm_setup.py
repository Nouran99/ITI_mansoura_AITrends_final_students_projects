# utils/llm_setup.py
from crewai import LLM

class GeminiModel:
    def __init__(self, config):
        self.llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=config['model']['api_key'],
            temperature=0.0
        )
    
    def get_llm(self):
        return self.llm
class GrokModel:
    def __init__(self, config):
        self.llm = LLM(
            model="groq/deepseek-r1-distill-llama-70b",
            api_key=config['model2']['api_key_grok'],
            temperature=0.0
        )
    
    def get_llm(self):
        return self.llm