from app.tools.search_tool import google_search
from app.model.ollama_wrapper import OllamaLLM
import os

class SearchAgent():
    def __init__(self, model: str = os.getenv('MODEL_NAME'), api_key: str = os.getenv('GOOGLE_API_KEY'), cx = os.getenv('SEARCH_ENGINE_ID')):
        self.api_key = api_key
        self.cx = cx
        self.llm = OllamaLLM(model)
    
    def search(self, learning_goal, objective):
        prompt = (
            f"The user wants to learn {learning_goal}. My specific objective is: {objective}.\n"
            "Give me one keyword or key phrase I can use to search for relevant learning materials.\n"
            "Output only the keyword or phrase. No explanations, no extra text."
        )
        return google_search(self.api_key, self.cx, self.llm.generate(prompt=prompt, temperature=.3))
    