from crewai import Agent
from tools.data_dashboard_tool import DataDashboardTool
from crewai import LLM
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyAm34w4wUcw5PASFuMqhqw-3ZCDHTjGybw"

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=os.environ.get("GEMINI_API_KEY")
)

dash_tool = DataDashboardTool()

dashboard_agent = Agent(
    role="Data Visualizer",
    goal="Generate visual insights from the data",
    backstory="An expert in crafting insightful dashboards and visual summaries.",
    tools=[dash_tool],
    verbose=True,
    llm=llm
)
