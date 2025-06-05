import streamlit as st
import pandas as pd
import ast
from crewai import Crew, Process # Import Crew and Process
from nutrition_agent import nutrition_agent, generate_meal_plan_task

st.title("🍽️ Nutrition Agent - Meal Plan Generator")

goal = st.selectbox("Goal", ["Lose Weight", "Gain Weight", "Maintain Weight"])
target_calories = st.number_input("Target Calories (kcal)", min_value=1000, max_value=5000, value=2000)
diet_type = st.selectbox("Diet Type", ["omnivore", "vegetarian", "keto", "vegan", "pescatarian"])

if st.button("Generate Meal Plan"):
  prompt = f"""
Goal: {goal}
Target Calories: {target_calories}
Diet Type: {diet_type}
"""
  # Create a Crew to run the task
  plan_crew = Crew(
      agents=[nutrition_agent],
      tasks=[generate_meal_plan_task],
      process=Process.sequential,
      verbose=True  # Set to True for detailed logs
  )

  # Kickoff the Crew with the inputs
  response = plan_crew.kickoff(inputs={'prompt': prompt})


  st.subheader("Generated Meal Plan")

  try:
      # Convert string output (Python list of dicts) to Python object
      meal_plan = ast.literal_eval(response)

      # Convert to DataFrame
      df = pd.DataFrame(meal_plan)

      # Optional: reorder columns or rename nicely
      columns_order = ['meal_type', 'name', 'description', 'estimated_calories', 'protein_g', 'carbs_g', 'fats_g', 'recipe_link']
      df = df[columns_order]

      # Show dataframe in Streamlit
      st.dataframe(df)

  except Exception as e:
      st.error(f"Failed to parse or display meal plan output: {e}")
