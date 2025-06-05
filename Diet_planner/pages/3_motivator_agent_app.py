import streamlit as st
import json
from motivator_agent import motivation_agent, motivate_user_task

st.title("💬 Motivational Coach Agent")

report_text = st.text_area(
    "Enter Tracker Agent Report JSON",
    height=200,
    value='{"compliance_score": "85%", "status": "Partially met goals", "macro_gaps": {"calories": -150, "protein_g": -10, "carbs_g": 5, "fats_g": -8}, "recommendations": ["Increase protein intake with a snack or shake", "Reduce simple carbs at lunch", "Try to meet calorie target to avoid under-fueling"]}'
)

if st.button("Generate Motivation"):
    try:
        report_json = json.loads(report_text)
        response = motivation_agent.run_task(motivate_user_task, inputs={"report": json.dumps(report_json)})
        st.subheader("Motivational Message")
        st.write(response)
    except Exception as e:
        st.error(f"Invalid input or error: {e}")
