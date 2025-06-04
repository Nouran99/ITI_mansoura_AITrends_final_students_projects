from crewai import Agent, Task, Crew
from src.models.model import GeminiModel
from src.agents.swot_agent import create_swot_agent
from src.agents.marketing_agent import create_marketing_agent
from src.agents.content_agent import create_content_agent
import yaml

def load_config():
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    gemini_model = GeminiModel(config)
    
    swot_agent = create_swot_agent(gemini_model)
    marketing_agent = create_marketing_agent(gemini_model)
    content_agent = create_content_agent(gemini_model)
    
    swot_task = Task(
        description=f"Analyze {config['company']['name']} in {config['company']['industry']} industry. Provide SWOT analysis with strengths, weaknesses, opportunities, and threats.",
        agent=swot_agent,
        expected_output="Detailed SWOT analysis report"
    )
    
    marketing_task = Task(
        description="Create marketing plan based on the SWOT analysis results",
        agent=marketing_agent,
        expected_output="Comprehensive marketing strategy"
    )
    
    content_task = Task(
        description="Plan content strategy for the marketing campaign",
        agent=content_agent,
        expected_output="Content calendar and strategy"
    )
    
    crew = Crew(
        agents=[swot_agent, marketing_agent, content_agent],
        tasks=[swot_task, marketing_task, content_task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    with open('data/processed/marketing_analysis.md', 'w') as f:
        f.write(str(result))

    
    print("Analysis complete. Results saved to data/processed/marketing_analysis.txt")

if __name__ == "__main__":
    main()