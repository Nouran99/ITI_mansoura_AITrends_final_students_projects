import streamlit as st

st.set_page_config(page_title="AI Diet Planner", layout="wide")
st.title("🥗 AI-Powered Diet Planner")
st.write("Welcome to your personalized diet assistant powered by intelligent agents. Use the menu on the left to explore:")
st.markdown("""
1.  **Home** - This page
2.  **Nutrition Agent - Meal Plan Generator** - Generate personalized meal plans.
3.  **Nutrition Tracker Agent - Intake & Activity Analysis** - Analyze your daily food intake and activity.
4.  **Motivational Coach Agent** - Get motivational messages based on your progress.
""")
st.markdown(
"""
<style>
/* Primary Color */
.stButton>button {
    background-color: #8be9fd;
    color: #000000;
}
/* Background Colors */
.css-1d391kg {
    background-color: #f8f9fa;
}
.css-18e3th9 {
    background-color: #ffffff;
}
/* Text color */
.css-10trblm {
    color: #000000;
}
</style>
""", unsafe_allow_html=True
)
