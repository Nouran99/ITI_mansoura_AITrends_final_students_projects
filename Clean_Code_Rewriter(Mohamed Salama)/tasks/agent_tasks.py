# tasks/agent_tasks.py
from crewai import Task

def analysis_task(agent, code):
    return Task(
        description=f"""
        Analyze the provided {code} for clean code violations 
        using Robert C. Martin's Clean Code principles. Identify issues such as poor naming conventions, complex logic, and lack of comments.
        Provide a structured analysis report with identified issues and suggestions for the generator agent and educator agent.
    """,
        expected_output="A detailed analysis report identifying specific Clean Code violations with locations and descriptions.",
        agent=agent
    )


def create_refactoring_task(agent, code):
    return Task(
        description=f"""Refactor the {code} based on the analysis report to improve its quality.
          But keep the original as it does not change the functionality.
          
          """,
        expected_output="Complete refactored code that addresses all identified issues while preserving functionality.",
        agent=agent,
        dependencies=[analysis_task]
    )

def create_education_task(agent, code):
    return Task(
        description=f"""Provide educational content about the identified issues from the analysis report.
        but provide the content based on the analysis report only that provided according to {code}.
        provide the lessons after the refactoring task is completed, and the generated code is provided.""",
        # This task does not depend on the analysis task, as it is meant to provide general clean code lessons
        expected_output="""
        1- **output code of the refactoring task**
        2- Educational content explaining Clean Code principles and best practices relevant to the analyzed code.
        """,
        agent=agent,
        dependencies=[analysis_task]
    )
# tasks/agent_tasks.py

# from crewai import Task


# def create_code_improvement_task(manager_agent, workers, code):
#     """
#     Create a unified manager-led task for analyzing, refactoring, and educating about code
#     following Clean Code principles.

#     Args:
#         manager_agent (Agent): The AI project manager agent.
#         code (str): The messy Python code to be improved.

#     Returns:
#         Task: The top-level task to be executed by the manager agent.
#     """

#     return Task(
#         description="\n".join([
#             f"You are tasked with managing the improvement of the following Python {code}:\n\n```python\n{code}\n```",
#             "",
#             "Coordinate the following subtasks with the appropriate specialist agents:",
#             "",
#             "**1. Code Analysis (Analyzer Agent)**",
#             "- Evaluate the {code} for Clean Code violations using Robert C. Martin’s principles",
#             "- Identify issues like poor naming, complexity, duplication, unclear formatting, or code smells",
#             "",
#             "**2. Refactoring (Generator Agent)**",
#             "- Refactor the {code} to address all issues found in the analysis",
#             "- Ensure functionality remains unchanged",
#             "- Follow Clean Code best practices: clear naming, simplicity, modular functions, etc.",
#             "",
#             "**3. Education (Educator Agent)**",
#             "- Based on the analysis, provide lessons to help developers understand and avoid such issues",
#             "- Include best practices, concise tips, and simple examples",
#             "",
#             "Ensure the final output is structured in this order:",
#             "1. The original {code}",
#             "2. The refactored version",
#             "3. Clean Code lessons from the educator agent",
#             "",
#             "Deliver a high-quality, readable, and educational final report."
#         ]),
#         expected_output="\n".join([
#             "A complete improvement report consisting of:",
#             "1. The original {code}",
#             "2. The clean, refactored code",
#             "3. Educational content explaining the issues and best practices"
#         ]),
#         agent=manager_agent
#     )
