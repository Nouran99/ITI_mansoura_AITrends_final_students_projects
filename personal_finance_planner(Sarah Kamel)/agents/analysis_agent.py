# analysis_agent.py

class AnalysisAgent:
    def __init__(self, llm_model):
        self.llm = llm_model

    def analyze(self, user_data_prompt):
        system_prompt = (
            "You are a financial analyzer. Your task is to analyze the user's financial data and provide the analysis. "
            "Break down the budget, evaluate expenses and percentage of expenditure of each item of income."
        )

        response = self.llm.chat_completion(
            system=system_prompt,
            user=user_data_prompt,
            temperature=0.1
        )

        return response
