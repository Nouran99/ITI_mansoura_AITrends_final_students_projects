from crewai import Task
from agents import task_analyzer, schedule_builder, productivity_enhancer

def create_task_analysis_task(tasks_content):
    return Task(
        description=f"""
        Analyze these tasks and sort by deadline urgency:
        {tasks_content}
        
        Requirements:
        1. Extract deadlines and sort by urgency (most urgent first)
        2. Assign priority (High/Medium/Low) 
        3. Estimate time needed
        4. Keep output simple and clear
        """,
        agent=task_analyzer,
        expected_output="Simple task list sorted by deadline with priority and time estimates"
    )

def create_schedule_building_task(analyzed_tasks=None):
    return Task(
        description=f"""
        Create a simple daily schedule based on the analyzed tasks:
        
        {analyzed_tasks if analyzed_tasks else "Use the output from the task analyzer"}
        
        Requirements:
        1. Schedule urgent tasks in morning hours
        2. Create clear time slots
        3. Keep format simple and readable
        4. Use format: 9:00 AM - 11:00 AM: Task Name (2 hours) - High Priority
        """,
        agent=schedule_builder,
        expected_output="Clean schedule with time slots, task names, duration, and priority"
    )

def create_productivity_enhancement_task(schedule=None):
    return Task(
        description=f"""
        Create a To-Do List format schedule with checkboxes.
        
        {schedule if schedule else "Use the output from the schedule builder"}
        
        **CRITICAL:** Ensure EACH CHECKBOX ITEM IS ON ITS OWN SEPARATE LINE.
        
        Requirements:
        1. Format as a checkable to-do list using '☐' for checkboxes.
        2. Group by priority levels: HIGH, MEDIUM, LOW.
        3. Include time slots and duration for each task.
        4. Add breaks as separate items under 'BREAKS & PERSONAL'.
        5. Keep it clean and organized like a daily planner.
        """,
        agent=productivity_enhancer,
        expected_output="To-Do List format with each task on a new line, grouped by priority, with time slots assigned based on the actual input tasks from the user."
    )