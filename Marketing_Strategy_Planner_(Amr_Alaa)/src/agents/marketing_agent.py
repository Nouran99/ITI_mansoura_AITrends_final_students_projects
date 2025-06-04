from crewai import Agent

def create_marketing_agent(gemini_model):
    return Agent(
        role="Marketing Strategist",
        goal="Create comprehensive marketing plans and strategies",
        backstory="Experienced marketing professional with expertise in campaign planning",
        llm=gemini_model.get_llm(),
        verbose=True
    )