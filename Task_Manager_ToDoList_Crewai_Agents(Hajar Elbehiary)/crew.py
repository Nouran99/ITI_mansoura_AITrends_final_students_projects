from crewai import Crew, Process
from agents import task_analyzer, schedule_builder, productivity_enhancer
from tasks import create_task_analysis_task, create_schedule_building_task, create_productivity_enhancement_task

class ProductivityCrew:
    def __init__(self):
        self.task_analyzer = task_analyzer
        self.schedule_builder = schedule_builder
        self.productivity_enhancer = productivity_enhancer
    
    def run(self, tasks_content):
        # Create the tasks
        analysis_task = create_task_analysis_task(tasks_content)
        schedule_task = create_schedule_building_task()  # Will use output from previous task
        enhancement_task = create_productivity_enhancement_task()  # Will use output from previous task
        
        # Create and run the crew
        crew = Crew(
            agents=[self.task_analyzer, self.schedule_builder, self.productivity_enhancer],
            tasks=[analysis_task, schedule_task, enhancement_task],
            verbose=True,
            process=Process.sequential  # Tasks run in sequence, passing outputs forward
        )
        
        result = crew.kickoff()
        return result