from app.model.ollama_wrapper import OllamaLLM
from app.tools.read_answers import read_user_answers
import os

class AssessmentAgent:
    def __init__(self, model: str = os.getenv('MODEL_NAME')):
        self.llm = OllamaLLM(model)

    def generate_assessment(self, learning_goal: str) -> str:
        # Get user answers as a formatted string
        answers_text = read_user_answers()

        if not answers_text:
            return "[ERROR] No user answers found or file is empty."

        prompt = (
            f"The user wants to learn: {learning_goal}.\n\n"
            "They have rated their familiarity with various concepts as follows:\n"
            f"{answers_text}\n\n"
            "Your task is to analyze this data and provide a deep, thoughtful assessment of the user's current understanding.\n\n"
            "Focus on:\n"
            "- Which areas the user appears confident in\n"
            "- Which areas show clear knowledge gaps\n"
            "- How the familiar and unfamiliar concepts relate to each other\n"
            "- Any inconsistencies or contradictions (e.g., being familiar with advanced ideas but unfamiliar with prerequisites)\n\n"
            "Avoid simply restating what the user said. Instead, reason about what their answers imply about their learning journey so far.\n\n"
            "Do NOT suggest next steps, learning paths, or resources.\n"
            "Do NOT mention that you are analyzing something or writing an assessment — just write the assessment itself."
        )

        return self.llm.generate(prompt, temperature=0.6, max_tokens=500)
