# advice_agent.py

import os

class AdviceAgent:
    def __init__(self, llm_model, output_dir="output"):
        self.llm = llm_model
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_advice(self, analysis_text):
        system_prompt = (
            "You are a financial advisor and planner. Based on the user's financial analysis below, provide a structured savings plan, "
            "write the analysis you have received and clear recommendations and plan, and practical advice. Keep the language easy to understand."
        )

        response = self.llm.chat_completion(
            system=system_prompt,
            user=analysis_text,
            temperature=0.1
        )

        return response

    def save_report(self, advice_text, filename="financial_advice_report.txt"):
        report_path = os.path.join(self.output_dir, filename)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(advice_text.strip() + "\n")
        return report_path

    def run(self, analysis_text, report_name="financial_advice_report.txt"):
        advice = self.generate_advice(analysis_text)
        file_path = self.save_report(advice, report_name)
        return advice, file_path
