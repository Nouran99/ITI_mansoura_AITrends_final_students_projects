import streamlit as st
from app.agents.agent1_diagnostic import DiagnosticAgent
from app.tools.save_answers import save_user_answers
import os
def render_initial_view(defaults):
    learning_goal = st.text_input("What do you want to learn?", placeholder="e.g., Machine Learning, Photoshop...", help="Type any topic or skill you'd like to master. Keep it specific for better results!")

    # --- Step 1: Generate Diagnostic Questions ---
    if st.button("Get started") and learning_goal:
        # Reset everything on fresh start
        for key in list(st.session_state.keys()):
            if key not in defaults:
                del st.session_state[key]
        st.session_state.update(defaults)
        st.session_state.learning_goal = learning_goal

        agent = DiagnosticAgent(os.getenv('MODEL_NAME'))
        with st.spinner("Getting things ready..."):
            st.session_state.questions = agent.generate_questions(learning_goal) or "No questions"

    # --- Step 2: Display Diagnostic Questions ---
    if st.session_state.questions == "No questions":
        st.error("⚠️ Something went wrong while generating the questions. Please try again.")

    elif st.session_state.questions:
        st.markdown("### 📝 Check all the statements that describe you")
        st.markdown("_This helps us understand what you're already familiar with, so your plan can focus on what matters most._")
        for i, question in enumerate(st.session_state.questions):
            key = f"q_{i}"
            response = st.checkbox(f"{i+1}. {question}", key=key)
            st.session_state.user_answers[question] = "Yes" if response else "No"

        if st.session_state.user_answers:
            save_user_answers(st.session_state.user_answers)
            st.session_state.show_continue = True