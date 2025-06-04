from crewai import Agent
from tools.smart_preprocessing_tool import SmartPreprocessingTool
from crewai import LLM
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyAm34w4wUcw5PASFuMqhqw-3ZCDHTjGybw"

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=os.environ.get("GEMINI_API_KEY")
)

preprocess_tool = SmartPreprocessingTool()

preprocessing_agent = Agent(
    role="Data Cleaner",
    goal="Apply smart preprocessing and cleaning to the data",
    backstory="A machine learning engineer skilled in preparing data for modeling.",
    tools=[preprocess_tool],
    verbose=True,
    llm=llm
)
