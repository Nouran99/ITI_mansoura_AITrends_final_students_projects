import os
import json
from dotenv import load_dotenv
from crewai import Crew, Process
import agentops
from motivator_agent import motivation_agent, motivate_user_task

load_dotenv(dotenv_path="/content/drive/MyDrive/diet_planner/.env")

def test_motivation(tracking_report, user_name="User"):
    agentops_key = os.getenv("AGENTOPS_API_KEY")
    agentops.init(api_key=agentops_key, skip_auto_end_session=True)

    motivate_crew = Crew(
        agents=[motivation_agent],
        tasks=[motivate_user_task],
        process=Process.sequential,
        verbose=False
    )

    try:
        result = motivate_crew.kickoff(
            inputs={
                'tracking_report': tracking_report,
                'user_name': user_name
            }
        )
        output_str = result.raw if hasattr(result, 'raw') else str(result)
        print("Motivation agent output:", output_str)
    except Exception as e:
        print(f"Error in motivation agent: {e}")
        output_str = f"Error generating motivational message: {e}"

    agentops.end_session()
    return output_str

if __name__ == "__main__":
    dummy_tracking_report = {"calories_diff": -200, "advice": "Great job, keep it up!"}
    test_motivation(dummy_tracking_report)
