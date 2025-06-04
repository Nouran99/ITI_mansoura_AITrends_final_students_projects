import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json5
import regex as re
from llm_interface import ask_llm

class JobParserAgent:
    def __init__(self):
        pass

    def run(self, job_description: str) -> dict:
        prompt = f"""
You are a professional job analysis assistant.

Extract structured data from the following job description and return a **valid JSON object** with the fields below.

Use these formats and examples:

- "required_skills": List of technical and soft skills mentioned.
  Example: ["data visualization", "problem-solving", "team collaboration", "Python", ....]

- "required_experience": A short phrase like "5+ years in data analysis" or "Bachelor’s degree in Computer Science".

- "preferred_tools_or_technologies": List of tools, software, frameworks, or platforms.
  Example: ["TensorFlow", "Keras", "Docker", "AWS", ....]

- "keywords": List of important role-specific terms and responsibilities.
  Example: ["AI model deployment", "data preprocessing", "cloud infrastructure", "real-time analytics", ....]

Return only a valid JSON object without any explanations, markdown, or additional text.
Job description:
\"\"\"{job_description}\"\"\"
Return only a valid JSON object with keys:
- required_skills
- required_experience
- preferred_tools_or_technologies
- keywords
Make sure to include all relevant information from the job description in the JSON object.
"""
        raw_result = ask_llm(prompt)

        # 🛠️ Extract the first JSON block using robust regex
        for attempt in range(3):
            try:
                json_match = re.search(r'\{(?:[^{}]|\n|\\{|\\})*\}', raw_result)
                if not json_match:
                    raise ValueError("No JSON block found.")
                json_str = json_match.group(0)
                parsed = json5.loads(json_str)
                return parsed
            except Exception as e:
                if attempt == 1:
                    raise e
                raw_result = ask_llm("Return only valid JSON:\n" + raw_result)

