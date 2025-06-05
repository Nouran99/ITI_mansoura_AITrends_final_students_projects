import os
import json
from dotenv import load_dotenv
from crewai import Crew, Process
import agentops
from tracker_agent import tracker_agent, evaluate_nutrition_task

load_dotenv(dotenv_path="/content/drive/MyDrive/diet_planner/.env")

def test_tracker(planned_intake, actual_intake, burned_calories=500):
    agentops_key = os.getenv("AGENTOPS_API_KEY")
    agentops.init(api_key=agentops_key, skip_auto_end_session=True)

    track_crew = Crew(
        agents=[tracker_agent],
        tasks=[evaluate_nutrition_task],
        process=Process.sequential,
        verbose=False
    )

    try:
        result = track_crew.kickoff(
            inputs={
                'planned_intake': planned_intake,
                'actual_intake': actual_intake,
                'burned_calories': burned_calories
            }
        )
        output_str = result.raw if hasattr(result, 'raw') else str(result)
        data = json.loads(output_str)
        print("Tracking evaluation JSON parsed successfully.")
    except Exception as e:
        print(f"Error in tracker agent: {e}")
        print("Raw output:", output_str)

    agentops.end_session()
    return output_str

if __name__ == "__main__":
    # Dummy test data
    planned = [{"name": "Oatmeal", "calories": 300}]
    actual = [{"name": "Oatmeal", "calories": 320}]
    test_tracker(planned, actual)
