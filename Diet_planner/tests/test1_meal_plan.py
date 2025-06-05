import os
import json
import re
import pandas as pd
from dotenv import load_dotenv
from crewai import Crew, Process
import agentops
from nutrition_agent import nutrition_agent, generate_meal_plan_task
from tabulate import tabulate

load_dotenv(dotenv_path="/content/drive/MyDrive/diet_planner/.env")

def extract_json(text):
    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None
    return None

def test_meal_plan(goal="lose weight", calories=1800, diet_type="vegetarian"):
    agentops_key = os.getenv("AGENTOPS_API_KEY")
    agentops.init(api_key=agentops_key, skip_auto_end_session=True)

    plan_crew = Crew(
        agents=[nutrition_agent],
        tasks=[generate_meal_plan_task],
        process=Process.sequential,
        verbose=False
    )

    try:
        result = plan_crew.kickoff(
            inputs={'goal': goal, 'calories': calories, 'diet_type': diet_type}
        )
        output_str = result.raw if hasattr(result, 'raw') else str(result)

        data = extract_json(output_str)
        if data is None:
            print("Failed to parse JSON from agent output.")
            print("Raw output:", output_str)
        else:
            print("Meal Plan JSON parsed successfully.")

            if isinstance(data, dict):
                meals = data.get('meals', data)
            elif isinstance(data, list):
                meals = data
            else:
                meals = []

            if isinstance(meals, list) and meals:
                df = pd.DataFrame(meals)
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            else:
                print("Parsed JSON does not contain a list of meals or meals list is empty.")
                print(meals)

    except Exception as e:
        print(f"Error in meal plan agent: {e}")
        print("Raw output:", output_str)

    agentops.end_session()
    return output_str

if __name__ == "__main__":
    test_meal_plan()
