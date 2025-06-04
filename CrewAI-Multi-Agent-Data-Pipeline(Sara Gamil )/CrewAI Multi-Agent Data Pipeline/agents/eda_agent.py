from crewai import Agent
from tools.explore_csv_tool import ExploreCSVDataTool
from crewai import LLM
import os


os.environ["GEMINI_API_KEY"] = "AIzaSyAm34w4wUcw5PASFuMqhqw-3ZCDHTjGybw"

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=os.environ.get("GEMINI_API_KEY")
)

explore_tool = ExploreCSVDataTool()

eda_agent = Agent(
    role="Data Analyst",
    goal="Generate a complete data exploration report for the given CSV",
    backstory="An expert in quickly understanding datasets and summarizing insights.",
    tools=[explore_tool],
    verbose=True,
    llm=llm
)
