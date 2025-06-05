from app.model.ollama_wrapper import OllamaLLM
import os

class CurriculumAgent:
    def __init__(self, model: str = os.getenv('MODEL_NAME')):
        self.llm = OllamaLLM(model)

    def generate_learning_plan(self, learning_goal: str, assessment: str) -> str:
        prompt = (
            f"The user wants to learn: {learning_goal}.\n\n"
            f"The following assessment outlines their current knowledge and gaps:\n"
            f"{assessment}\n\n"
            "Your task is to create a personalized, structured 4-week learning plan. "
            "Incorporate both the insights from the assessment and foundational principles typically found in expert learning roadmaps for this subject.\n\n"
            "For each week:\n"
            "- Write a clear learning objective that reflects both the user's needs and logical progression in skill development.\n"
            "- List several key topics the user should focus on. For each topic, clarify the intended learning activity using concise descriptions like 'read foundational concepts', 'watch a visual explanation', or 'review prior knowledge'. Avoid parenthetical labels or formatting tags.\n"
            "- List several practical tasks designed to reinforce understanding. Describe these using natural language instructions, such as 'solve problems involving...', 'implement a simple version of...', or 'experiment with...'.\n\n"
            "Avoid using placeholder phrases, bullet-point templates, or specific resource names. Structure the output as clear, labeled weekly segments in well-organized plain text.\n"
            "Your response should sound like a coach outlining a real study plan—personalized, progressive, and grounded in sound pedagogy."
        )

        return self.llm.generate(prompt, temperature=0.42, max_tokens=1024)
