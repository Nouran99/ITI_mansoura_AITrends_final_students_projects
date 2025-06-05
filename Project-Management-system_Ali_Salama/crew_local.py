from crewai import Crew, Process
from agents import AgileProjectAgents
from tasks import AgileProjectTasks

class AgileProjectCrew:
    def __init__(self):
        self.agents = AgileProjectAgents()
        self.tasks = AgileProjectTasks()
    
    def create_crew(self, project_description):
        # Initialize all agents
        customer_listener = self.agents.customer_listener_agent()
        requirement_extractor = self.agents.requirement_extractor_agent()
        planner = self.agents.planning_milestone_agent()
        story_generator = self.agents.user_story_generator_agent()
        tech_advisor = self.agents.technology_advisor_agent()
        packager = self.agents.plan_packager_agent()

        
        # Create tasks with dependencies
        intake_task = self.tasks.customer_intake_task(
            agent=customer_listener,
            project_description=project_description
        )
        
        requirements_task = self.tasks.extract_requirements_task(
            agent=requirement_extractor,
            context=[intake_task]
        )
        
        planning_task = self.tasks.create_project_plan_task(
            agent=planner,
            context=[requirements_task]
        )
        
        stories_task = self.tasks.generate_user_stories_task(
            agent=story_generator,
            context=[requirements_task, planning_task]
        )
        
        tech_task = self.tasks.recommend_tech_stack_task(
            agent=tech_advisor,
            context=[requirements_task]
        )
        
        
        package_task = self.tasks.package_project_plan_task(
            agent=packager,
            context=[intake_task, requirements_task, planning_task, 
                    stories_task, tech_task]
        )


        # Create and return crew
        return Crew(
            agents=[customer_listener, requirement_extractor, planner,
                   story_generator,tech_advisor, packager],
            tasks=[intake_task, requirements_task, planning_task,
                  stories_task,tech_task, package_task],
            process=Process.sequential,
            verbose=False
        )
    
    def run(self, project_description):
        crew = self.create_crew(project_description)
        result = crew.kickoff()
        return result