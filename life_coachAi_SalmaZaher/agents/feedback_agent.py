# agents/feedback_agent.py
from llm.llm_interface import generate_feedback

def analyze_day(user_log):
    """
    Analyze the user's log and return motivational feedback.
    """
    response = generate_feedback(user_log)
    return response
