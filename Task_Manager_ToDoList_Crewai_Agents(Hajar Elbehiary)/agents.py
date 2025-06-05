from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Setup LLM
from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

# Task Analyzer Agent
task_analyzer = Agent(
    role='Task Analyzer',
    goal='Sort tasks by deadline urgency and estimate time - keep output simple',
    backstory="""You are a practical task organizer who creates clear, simple task lists. 
    You prioritize by deadlines and give realistic time estimates.""",
    verbose=False,
    allow_delegation=False,
    llm=llm
)

# Schedule Builder Agent
schedule_builder = Agent(
    role='Schedule Builder',
    goal='Create simple daily schedules with clear time slots',
    backstory="""You are a time management expert who creates clean, easy-to-follow schedules. 
    You put urgent tasks first and use simple time formats.""",
    verbose=False,
    allow_delegation=False,
    llm=llm
)

# Productivity Enhancer Agent
productivity_enhancer = Agent(
    role='Productivity Enhancer',
    goal='Add essential breaks and practical tips - keep it simple',
    backstory="""You are a productivity coach who believes in simplicity. 
    You add necessary breaks and give one useful tip.""",
    verbose=False,
    allow_delegation=False,
    llm=llm
)