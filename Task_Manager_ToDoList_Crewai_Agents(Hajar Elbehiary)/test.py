from crew import ProductivityCrew

# User's tasks
tasks_content = """
- Finish quarterly report (Due: Tomorrow)
- Weekly team meeting (Due: Today at 2pm)
- Email client proposal (Due: Friday)
- Research new software options (Due: Next week)
"""

# Create and run the crew
productivity_crew = ProductivityCrew()
result = productivity_crew.run(tasks_content)
print(result)