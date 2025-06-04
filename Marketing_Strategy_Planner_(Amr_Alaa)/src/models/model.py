from crewai import LLM

class GeminiModel:
    def __init__(self, config):
        self.llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=config['model']['api_key']
        )
    
    def get_llm(self):
        return self.llm