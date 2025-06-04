from crewai import Agent
from tools.model_suggestion_tool import ModelSuggestionTool
from crewai import LLM
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyAm34w4wUcw5PASFuMqhqw-3ZCDHTjGybw"

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=os.environ.get("GEMINI_API_KEY")
)

model_tool = ModelSuggestionTool()

model_suggestion_agent = Agent(
    role="ML Expert",
    goal="Analyze data and recommend the best models using both insights and community trends.",
    backstory="A senior ML researcher who studies data deeply and checks Kaggle/GitHub trends before choosing models.",
    tools=[model_tool],
    verbose=True,
    llm=llm
)
