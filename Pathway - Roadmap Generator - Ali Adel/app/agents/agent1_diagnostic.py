from app.model.ollama_wrapper import OllamaLLM
from app.tools.json_tools import extract_json_list
import os

class DiagnosticAgent:
    def __init__(self, model: str = os.getenv('MODEL_NAME')):
        self.llm = OllamaLLM(model)

    def generate_questions(self, learning_goal: str, num_questions: int = 10) -> list:
        prompt = (
            f"The user wants to learn: {learning_goal}.\n"
            f"Generate {num_questions} simple diagnostic statements starting with "
            f"'I'm familiar with...' for example. Each one should reflect a core concept or skill relevant to the goal.\n"
            "Return only a JSON array of strings. Do not include explanations or markings"
        )


        response = self.llm.generate(prompt, temperature=0.3)
        questions = extract_json_list(response)
        return questions
