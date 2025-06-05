import streamlit as st
from app.agents.agent3_curriculum import CurriculumAgent
import os

def render_plan():
    if st.session_state.assessment_result and not st.session_state.plan_result:
        curriculum_agent = CurriculumAgent(os.getenv('MODEL_NAME'))
        with st.spinner("Generating your personalized 4-week learning plan..."):
            st.session_state.plan_result = curriculum_agent.generate_learning_plan(
                st.session_state.assessment_result,
                st.session_state.learning_goal
            )

    # --- Step 6: View Plan (Text) ---
    if st.session_state.plan_result:
        with st.expander("📝 Full Plan (Text Version)", expanded=False):
            st.write(st.session_state.plan_result)