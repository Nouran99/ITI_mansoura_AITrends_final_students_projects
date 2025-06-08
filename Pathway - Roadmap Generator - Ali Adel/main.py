import streamlit as st
from app.views.initial_view import render_initial_view
from app.views.reasoning_view import render_user_reasoning
from app.views.plan_view import render_plan
from app.views.interactive_plan_view import render_interactive_plan
from app.views.resources_view import render_resources_view
from app.views.footer import render_footer
from dotenv import load_dotenv
import os

load_dotenv()


# --- Page Config ---
st.set_page_config(page_title="AI Learning Coach", layout="centered")
st.markdown("# 🛤️ Pathway")
st.markdown("### A simple step-by-step guide to help you learn anything effectively.")
st.markdown("#### 🎯 Define Your Learning Goal")
st.markdown(
    "Whether you're just starting out or picking up something new, **Pathway** will guide you through a simple, structured plan. "
    "No pressure. Just steady progress, built around your goals."
)

# --- Initialize Session State ---
defaults = {
    "questions": [],
    "user_answers": {},
    "show_continue": False,
    "assessment_result": "",
    "plan_result": "",
    "json_plan": "",
    "learning_goal":"",
    "saved_answers":[],
    "resources_fetched":False
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

render_initial_view(defaults)
render_user_reasoning()
render_plan()
render_interactive_plan()
render_resources_view()
render_footer()
