from crewai import Agent, Task, Crew
from agents.resume_matcher import ResumeParserAgent
from agents.job_parser import JobParserAgent
from agents.resume_matcher import MatchAgent

resume_agent = Agent(name="ResumeParserAgent", role="Extracts skills from resumes", backstory="A skillful extractor for parsing CVs.")
job_agent = Agent(name="JobParserAgent", role="Extracts key requirements from job descriptions", backstory="Expert in HR language and job ads.")
match_agent = Agent(name="MatchAgent", role="Matches resume skills with job requirements", backstory="Experienced recruiter AI.")

resume_task = Task(agent=resume_agent, expected_output="Extracted list of skills from resume")
job_task = Task(agent=job_agent, expected_output="Extracted list of skills from job description")
match_task = Task(agent=match_agent, expected_output="List of missing and matched skills")

crew = Crew(
    agents=[resume_agent, job_agent, match_agent],
    tasks=[resume_task, job_task, match_task],
    verbose=True
)
