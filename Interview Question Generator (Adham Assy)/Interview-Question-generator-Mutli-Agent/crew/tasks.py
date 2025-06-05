from crewai import Task
from .agents import cv_agent, role_agent, question_agent

cv_task = Task(
    agent=cv_agent,
    description=(
        """Parse the uploaded CV PDF from the provided path and extract the following details:
        - List of technical skills
        - Academic degrees and major fields
        - Technical projects with titles and brief summaries
        - Completed courses and certifications
        - Internships or work experience with responsibilities"""
    ),
    expected_output=(
        "A JSON object with keys: skills, education, projects, courses, internships, experience"
    )

)


role_task = Task(
    agent=role_agent,
    description=(
        "Given a job title and description, extract the technical expectations including required skills, tools, knowledge areas, responsibilities, and preferred qualifications."
    ),
    expected_output=(
        "A JSON object with keys: required_skills, preferred_tools, knowledge_areas, responsibilities, prerequisites"
    )
)


question_task = Task(
    agent=question_agent,
    description=(
        """Based on the extracted CV data and the role profile, generate 10-15 technical interview questions that test:
        - Skills mentioned in the CV and required by the job
        - Projects listed in the CV
        - Relevant courses or certifications
        - Internships or job experiences
        - Problem-solving and applied knowledge in the job context"""
    ),
    expected_output=(
        "A list of 10-15 categorized technical interview questions in JSON format with categories like 'Skills', 'Projects', 'Experience', etc."
    )
)