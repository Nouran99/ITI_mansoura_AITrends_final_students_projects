# crew_make.py
from crewai import Crew, Process
from agents.anlyzer import create_analyst_agent
from agents.generator import create_modifier_agent
from agents.teacher import create_educator_agent
from agents.manger import create_manager_agent  # Import manager agent if needed, but not used in this workflow
# Remove unused manager import
from tasks.agent_tasks import analysis_task, create_refactoring_task, create_education_task
import yaml
from utils.llm_setup import GeminiModel, GrokModel  # Assuming this is the correct import path

def load_config():
    with open('utils/config.yaml', 'r') as f:
        return yaml.safe_load(f)
config = load_config()
gemini_model = GeminiModel(config)
grok_model = GrokModel(config)
def run_code_improvement_workflow(code):
    # Create agents
    analyst = create_analyst_agent(gemini_model)
    modifier = create_modifier_agent(gemini_model)
    educator = create_educator_agent(grok_model)
    manger = create_manager_agent(grok_model)  # Import manager agent if needed, but not used in this workflow

    # Create tasks
    analysistask = analysis_task(analyst, code)
    refactoring_task = create_refactoring_task(modifier, code)
    education_task = create_education_task(educator, code)

    # Create and run the crew
    crew = Crew(
        description="A crew of AI agents working together to analyze, refactor, and educate about messy Python code.",
        agents=[manger,analyst, modifier, educator],
        tasks=[analysistask, refactoring_task, education_task],
        verbose=False,
        process=Process.sequential,
        name="Code Improvement Crew",
        manager_agent=manger,
        
    )

    result = crew.kickoff()
    return result