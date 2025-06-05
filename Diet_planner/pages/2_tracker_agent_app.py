import streamlit as st
import json
from tracker_agent import tracker_agent, evaluate_nutrition_task

st.title("📊 Nutrition Tracker Agent - Intake & Activity Analysis")

planned_intake_text = st.text_area(
    "Planned Intake (JSON list of meals with 'name', 'calories', 'protein_g', 'carbs_g', 'fats_g')",
    height=150,
    value='[{"name": "Chicken Salad", "calories": 350, "protein_g": 30, "carbs_g": 10, "fats_g": 15}]'
)

actual_intake_text = st.text_area(
    "Actual Intake (JSON list of meals with 'name', 'calories', 'protein_g', 'carbs_g', 'fats_g')",
    height=150,
    value='[{"name": "Chicken Salad", "calories": 400, "protein_g": 35, "carbs_g": 12, "fats_g": 18}]'
)

burned_calories = st.number_input("Calories Burned Today", min_value=0, value=300)

if st.button("Evaluate Compliance"):
    try:
        planned_intake = json.loads(planned_intake_text)
        actual_intake = json.loads(actual_intake_text)
    except Exception as e:
        st.error(f"Invalid JSON input: {e}")
        planned_intake = None
        actual_intake = None

    if planned_intake and actual_intake:
        inputs = {
            "planned_intake": planned_intake,
            "actual_intake": actual_intake,
            "burned_calories": burned_calories,
        }
        report = tracker_agent.run_task(evaluate_nutrition_task, inputs=inputs)
        st.subheader("Daily Nutrition Compliance Report")
        if isinstance(report, str):
            try:
                report_json = json.loads(report)
                st.json(report_json)
            except:
                st.text(report)
        else:
            st.json(report)
