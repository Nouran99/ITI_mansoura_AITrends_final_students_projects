from crewai import Agent, LLM
from utils.base_model import llm

class AgileProjectAgents:
    def __init__(self):
        """Initialize with a selected LLM provider and model"""
        self.llm = llm
    
    def customer_listener_agent(self):
        return Agent(
            role='Customer Requirements Specialist',
            goal='Collect and understand customer requirements, goals, and constraints for their project',
            backstory="""You are an experienced business analyst who excels at 
            understanding customer needs. You ask the right questions to gather 
            comprehensive project requirements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def requirement_extractor_agent(self):
        return Agent(
            role='Requirements Analyst',
            goal='Convert customer input into structured functional and non-functional requirements',
            backstory="""You are a senior requirements analyst with expertise in 
            breaking down business needs into clear, actionable requirements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def planning_milestone_agent(self):
        return Agent(
            role='Agile Project Planner',
            goal='Create sprint plans, milestones, and project timeline',
            backstory="""You are a certified Scrum Master with years of experience 
            in planning and organizing agile projects. You excel at breaking down 
            projects into manageable sprints.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def user_story_generator_agent(self):
        return Agent(
            role='User Story Creator',
            goal='Generate detailed user stories with acceptance criteria',
            backstory="""You are an experienced product owner who writes clear, 
            concise user stories that development teams love. You always include 
            comprehensive acceptance criteria.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def technology_advisor_agent(self):
        return Agent(
            role='Technical Architecture Advisor',
            goal='Recommend optimal technology stack based on requirements and constraints',
            backstory="""You are a solutions architect with deep knowledge of 
            modern tech stacks. You consider scalability, cost, and team expertise 
            when making recommendations.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def plan_packager_agent(self):
        return Agent(
            role='Project Documentation Specialist',
            goal='Compile all project information into a comprehensive, professional project plan that meets stakeholder expectations and industry standards',
            backstory="""You are a senior technical writer with 10+ years of experience in 
            software project documentation. You excel at transforming complex technical 
            information into clear, actionable documentation that both technical teams 
            and business stakeholders can understand and act upon. Your documentation 
            has helped secure funding for numerous successful projects.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )