import streamlit as st
from app.agents.agent2_assessment import AssessmentAgent
import os

def render_user_reasoning():
    # --- Step 3: Generate Assessment ---
    if st.session_state.show_continue and st.button("Generate plan"):
        # Reset only what needs to be recomputed
        st.session_state["assessment_result"] = ""
        st.session_state["plan_result"] = ""
        st.session_state["json_plan"] = ""

        # Also reset all checkbox states (topics + tasks)
        keys_to_clear = [key for key in st.session_state.keys() if key.startswith("w") and ("_task_" in key or "_topic_" in key)]
        for key in keys_to_clear:
            st.session_state[key] = False


        assessment_agent = AssessmentAgent(os.getenv('MODEL_NAME'))
        with st.spinner("Analyzing..."):
            st.session_state.assessment_result = assessment_agent.generate_assessment(st.session_state.learning_goal)

    # --- Step 4: View Assessment ---
    if st.session_state.assessment_result:
        with st.expander("🔍 Breakdown of Your Skill Analysis", expanded=False):
            st.write(st.session_state.assessment_result)