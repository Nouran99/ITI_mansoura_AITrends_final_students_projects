import streamlit as st

def save_user_answers(answers: dict):
    """
    Save user answers to Streamlit session state.
    """
    try:
        st.session_state["saved_answers"] = answers.copy()
        print("[INFO] Answers saved to session state")
    except Exception as e:
        print(f"[ERROR] Could not save answers to session state: {e}")
