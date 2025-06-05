from crewai import Agent
from config.llm_config import llm

class BaseAgent:
    def __init__(self, role, goal, backstory, tools=None):
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            llm=llm.client,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def get_agent(self):
        return self.agent