from crewai.tools import BaseTool
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool

import seaborn as sns
import matplotlib.pyplot as plt

from typing import Optional 
# Assuming 'llm' is defined elsewhere as in the original notebook
import os
os.environ["SERPAPI_API_KEY"] = "5b052e700fa2d7a59b59bad4c7aa713589708babaa9c56cfeb94a7695feeae43"


from crewai.tools import BaseTool
from typing import Optional
from crewai import tools

from serpapi import GoogleSearch  # you can use SerpAPI to search Kaggle and GitHub

class KaggleGithubModelSearchTool(BaseTool):
    name: str = "Kaggle & GitHub Model Search Tool"
    description: str = "Searches Kaggle and GitHub to find the best models used for similar datasets."

    def _run(self, tool_input: Optional[str] = None) -> str:
        if not tool_input:
            return "No dataset keywords provided for search."

        results = []

        # Use Google Search API or SerpAPI to simulate Kaggle/GitHub search
        queries = [
            f"site:kaggle.com {tool_input} best machine learning models",
            f"site:github.com {tool_input} ML models used",
        ]
        for query in queries:
            search = GoogleSearch({
                "q": query,
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "num": 5
            })
            result = search.get_dict()
            links = [r['link'] for r in result.get('organic_results', [])]
            results.extend(links)

        if not results:
            return "No useful Kaggle or GitHub results found."

        formatted = "\n".join(results[:5])
        return f"Top related Kaggle/GitHub pages:\n{formatted}"


class ModelSuggestionTool(BaseTool):
    name: str = "Model Suggestion Tool"
    description: str = "Suggests the best ML models based on EDA, visual insights, and external sources (Kaggle/GitHub)."

    def _run(self, tool_input: Optional[str] = None) -> str:
        with open("eda_report.txt", "r", encoding="utf-8") as f1, open("dashboard_output/visual_insights.txt", "r", encoding="utf-8") as f2:
            eda = f1.read()
            vis = f2.read()

        # Combine EDA + Visuals
        insights = eda + "\n\n" + vis
        suggestions = ["🤖 **MODEL RECOMMENDATION REPORT** 🤖\n"]

        # Rule-based logic
        if "Outliers detected" in vis or "RobustScaler" in eda:
            suggestions.append("📌 Outliers detected. Recommended models: **Random Forest**, **XGBoost**.")

        if "Highly skewed" in vis or "Skewness" in vis:
            suggestions.append("📈 Skewed data. Suggested: **Gradient Boosting**, or transform + **Logistic Regression**.")

        if "🔗 Correlation Matrix" in eda and "1.00" in eda:
            suggestions.append("🔗 High multicollinearity. Use regularized models like **Lasso/Ridge**.")

        if "Target" in eda and "object" in eda:
            suggestions.append("🧠 Categorical target. Classification models like **XGBoost**, **Random Forest**, **Logistic Regression** recommended.")
        elif "Target" in eda:
            suggestions.append("📈 Numerical target. Regression models like **Linear Regression**, **XGBoost Regressor**.")

        if len(suggestions) == 1:
            suggestions.append("🔍 Not enough patterns detected. Start with **Random Forest** and **XGBoost**.")

        # Optional: Search Kaggle/GitHub
        
        search_tool = KaggleGithubModelSearchTool()
        external_findings = search_tool._run(tool_input)

        suggestions.append("\n🌐 **External Suggestions from Kaggle/GitHub:**\n" + external_findings)

        return "\n".join(suggestions)
