from crewai import Agent

def create_content_agent(gemini_model):
    return Agent(
        role="Content Planner",
        goal="Plan and strategize content for marketing campaigns",
        backstory="Creative content strategist with expertise in multi-channel content planning",
        llm=gemini_model.get_llm(),
        verbose=True
    )