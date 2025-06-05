from crewai import Agent
from Tools import Scraping_Tool1   


def Scraping_agent(llm):
    return Agent(
    role="Web scraping agent",
    goal="To extract details from any website",
    backstory="The agent is designed to help in looking for required values from any website url. These details will be used to decide which best product to buy.",
    llm=llm,
    tools=[Scraping_Tool1.web_scraping_tool],
    verbose=True
    )

