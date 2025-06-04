from crewai import Agent

def create_swot_agent(gemini_model):
    return Agent(
        role="SWOT Analyst",
        goal="Analyze company strengths, weaknesses, opportunities, and threats",
        backstory="Expert business analyst specializing in strategic analysis",
        llm=gemini_model.get_llm(),
        verbose=True
    )