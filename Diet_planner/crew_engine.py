import os
import json
from dotenv import load_dotenv
from crewai import Crew, Process
import agentops

from nutrition_agent import nutrition_agent, generate_meal_plan_task
from tracker_agent import tracker_agent, evaluate_nutrition_task
from motivator_agent import motivation_agent, motivate_user_task

load_dotenv(dotenv_path="/content/drive/MyDrive/diet_planner/.env")

def crew_plan(user_name="User", goal="lose weight", calories=1800, diet_type="vegetarian", actual_intake=None, burned_calories=500):
    # === Load keys ===
    gemini_key = os.getenv("GEMINI_API_KEY")
    agentops_key = os.getenv("AGENTOPS_API_KEY")

    # === Init AgentOps ===
    agentops.init(
        api_key=agentops_key,
        skip_auto_end_session=True
    )

    output_dir = "/content/drive/MyDrive/diet_planner/ai-agent-outpt"
    os.makedirs(output_dir, exist_ok=True)

    # === Step 1: Generate Meal Plan ===
    plan_crew = Crew(
        agents=[nutrition_agent],
        tasks=[generate_meal_plan_task],
        process=Process.sequential,
        verbose=False
    )

    if not goal or not calories or not diet_type:
        # Use a dictionary structure for consistency even with errors
        agentops.end_session() # Ensure session is ended on error
        return {"error": "Missing required inputs for meal planning."}


    try:
        meal_plan_result = plan_crew.kickoff(
            inputs={
                'goal': goal,
                'calories': calories,
                'diet_type': diet_type
            }
        )
         # Check if the result is a string or has a 'raw' attribute
        meal_plan_output_string = meal_plan_result.raw if hasattr(meal_plan_result, 'raw') else str(meal_plan_result)

        # Attempt to parse the output string
        planned_data = json.loads(meal_plan_output_string)
        planned_intake = planned_data.get("meals", []) # Adjust key based on actual output structure
    except Exception as e:
        print(f"Error during meal plan generation or parsing: {e}")
        agentops.end_session() # Ensure session is ended on error
        # Return an error or handle gracefully if meal plan generation fails
        return {"error": f"Failed to generate or parse meal plan: {e}", "meal_plan_raw_output": meal_plan_output_string if 'meal_plan_output_string' in locals() else "N/A"}


    # Use default intake if not passed
    if actual_intake is None:
        actual_intake = [
            {"name": "Oatmeal with banana", "calories": 340, "protein_g": 8, "carbs_g": 60, "fats_g": 6},
            {"name": "Veggie wrap", "calories": 400, "protein_g": 10, "carbs_g": 50, "fats_g": 12},
            {"name": "Lentil soup", "calories": 450, "protein_g": 20, "carbs_g": 40, "fats_g": 15},
            {"name": "Apple", "calories": 95, "protein_g": 0, "carbs_g": 25, "fats_g": 0},
            {"name": "Almonds", "calories": 160, "protein_g": 6, "carbs_g": 6, "fats_g": 14}
        ]

    # === Step 2: Track ===
    track_crew = Crew(
        agents=[tracker_agent],
        tasks=[evaluate_nutrition_task],
        process=Process.sequential,
        verbose=False
    )

    try:
        tracking_result = track_crew.kickoff(
            inputs={
                'planned_intake': planned_intake, # Pass the parsed planned intake
                'actual_intake': actual_intake,
                'burned_calories': burned_calories
            }
        )
        tracking_output_string = tracking_result.raw if hasattr(tracking_result, 'raw') else str(tracking_result)
        # Attempt to parse the tracking output
        tracking_data = json.loads(tracking_output_string)
    except Exception as e:
        print(f"Error during tracking evaluation or parsing: {e}")
        # Use an empty dict or handle as an error, but allow the process to continue to motivation
        tracking_data = {"error": f"Failed to evaluate or parse tracking: {e}", "tracking_raw_output": tracking_output_string if 'tracking_output_string' in locals() else "N/A"}


    # === Step 3: Motivate ===
    motivate_crew = Crew(
        agents=[motivation_agent],
        tasks=[motivate_user_task],
        process=Process.sequential,
        verbose=False
    )

    try:
        motivate_result = motivate_crew.kickoff(
            inputs={
                'tracking_report': tracking_data, # Pass the parsed tracking data (or error dict)
                'user_name': user_name
            }
        )
        motivate_output_string = motivate_result.raw if hasattr(motivate_result, 'raw') else str(motivate_result)
    except Exception as e:
        print(f"Error during motivation generation: {e}")
        motivate_output_string = f"Error generating motivational message: {e}"


    # === Save Outputs ===
    # Use the raw string outputs for saving to files
    try:
        with open(os.path.join(output_dir, "meal_plan_result.json"), "w") as f1:
            f1.write(meal_plan_output_string)

        with open(os.path.join(output_dir, "tracking_result.json"), "w") as f2:
            f2.write(tracking_output_string)

        with open(os.path.join(output_dir, "motivation_result.txt"), "w") as f3:
            f3.write(motivate_output_string)
    except Exception as e:
         print(f"Error saving results to files: {e}")


    agentops.end_session()

    return {
        "meal_plan": meal_plan_output_string,
        "tracking": tracking_output_string,
        "motivation": motivate_output_string
    }

print("crew_engine.py module loaded and crew_plan function defined.") # Add this line
