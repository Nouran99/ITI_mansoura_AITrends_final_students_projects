import streamlit as st

def read_user_answers() -> str:
    """
    Reads answers from st.session_state['saved_answers'] and formats them as:
    - "I'm familiar with X.": Yes
    - "I'm familiar with Y.": No
    Returns the entire block as a string for prompt injection.
    """
    answers = st.session_state.get("saved_answers", {})
    if not answers:
        print("[INFO] No saved answers in session state.")
        return ""

    lines = [f'- "{question}": {answer}' for question, answer in answers.items()]
    return "\n".join(lines)
