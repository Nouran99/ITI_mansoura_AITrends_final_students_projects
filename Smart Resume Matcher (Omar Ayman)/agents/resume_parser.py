from llm_interface import ask_llm

class ResumeParserAgent:
    def run(self, resume_text):
        prompt = f"""
        Extract only a JSON array of relevant skills from the following resume text:
        {resume_text}
        """
        return ask_llm(prompt)
