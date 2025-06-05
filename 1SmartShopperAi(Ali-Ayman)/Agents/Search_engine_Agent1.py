from Tools import Search_engine_tool0
from crewai import Agent    



def Search_engine_agent(llm):
    return Agent(
        role="Search Engine Agent",
        goal="To search for products based on the suggested search query",
        backstory="The agent is designed to help in looking for products by searching for products based on the suggested search queries.",
        llm=llm,
        verbose=True,
        tools=[Search_engine_tool0.search_engine_tool]
    )

