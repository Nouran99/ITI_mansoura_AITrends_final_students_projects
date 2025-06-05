from app.model.ollama_wrapper import OllamaLLM
from app.tools.json_tools import extract_json_plan, normalize_plan_structure
import os
class JsonConverterAgent:
    def __init__(self, model: str = os.getenv('MODEL_NAME')):
        self.llm = OllamaLLM(model)

    def convert_plan_to_json(self, plan_text: str) -> str:
        prompt = (
            "Below is a 4-week learning plan written in plain English.\n\n"
            "Convert this plan into a valid JSON array of week objects with the following structure:\n"
            "[\n"
            "  {\n"
            "    \"week_number\": 1,\n"
            "    \"objective\": \"...\",\n"
            "    \"topics\": [\"...\", \"...\"],\n"
            "    \"tasks\": [\"...\", \"...\"]\n"
            "  },\n"
            "  {\n"
            "    \"week_number\": 2,\n"
            "    \"objective\": \"...\",\n"
            "    \"topics\": [...],\n"
            "    \"tasks\": [...]\n"
            "  },\n"
            "  ...\n"
            "]\n\n"
            "Do not include any extra text, explanations, or formatting. Output only the raw JSON array.\n\n"
            f"{plan_text}"
        )
        
        return normalize_plan_structure(extract_json_plan(self.llm.generate(prompt, temperature=0.2, max_tokens=1024)))
