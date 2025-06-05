from crewai import Task
import os


def final_Reporter_task(final_reporter_agent) -> Task:
    """
    Creates a CrewAI Task to generate a professional HTML procurement report
    based on scraped product search results.

    Parameters:
    ----------
    final_reporter_agent : Agent
        The agent responsible for generating the HTML report.

    Returns:
    -------
    Task
        A configured CrewAI Task to generate a structured and styled procurement report.
    """

    # Set up output directory and file path
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data'))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "step_4_final_report.json")

    # Task description
    description = "\n".join([
        "Generate a professional HTML procurement report based on the collected product search results.",
        "Use the Bootstrap CSS framework to ensure a clean and responsive UI.",
        "Incorporate provided company context to tailor the report appropriately.",
        "The report should include data from multiple websites, including prices and product details.",
        "Ensure each product in the report includes its direct purchase link.",
        "Create a clickable link for each product for easy reference.",
        "Structure the HTML report with the following sections:",
        "1. Executive Summary: Brief overview of the procurement process and key insights.",
        "2. Introduction: Purpose and scope of the report.",
        "3. Methodology: Techniques used for data gathering and comparison.",
        "4. Findings: Detailed comparison (tables/charts) of products across sites.",
        "5. Analysis: Interpret the findings, highlight trends and anomalies.",
        "6. Recommendations: Procurement decisions based on analysis.",
        "7. Conclusion: Summary and final remarks.",
        "8. Appendices: Raw data or any supplementary materials."
    ])

    return Task(
        description=description,
        expected_output="A complete and professionally designed HTML page for the procurement report.",
        output_file=output_path,
        agent=final_reporter_agent
    )
