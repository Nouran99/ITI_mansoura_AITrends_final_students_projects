import streamlit as st
from app.agents.agent5_search import SearchAgent
import os

def render_resources_view():
    # --- Step 9: Reccomend Resoueces ---
    learning_goal = st.session_state.get("learning_goal")
    plan = st.session_state.get("json_plan")
    all_results = st.session_state.get("resources_fetched")

    if learning_goal and plan:
        
        if not all_results:
            search_agent = SearchAgent(os.getenv('MODEL_NAME'))

            all_results = []

            with st.spinner("Fetching resource recommendations..."):
                for week in plan:
                    week_num = week["week_number"]
                    objective = week["objective"]
                    results = search_agent.search(learning_goal, objective)

                    all_results.append({
                        "week_number": week_num,
                        "objective": objective,
                        "results": results
                    })
            st.session_state["resources_fetched"] = all_results
            
        # Now render all expanders at once
        st.markdown("### 🔍 Resources You May Find Helpful")
        for week_data in all_results:
            with st.expander(f"📅 Week {week_data['week_number']}"):
                if not week_data["results"]:
                    st.info("No relevant resources found.")
                else:
                    for res in week_data["results"]:
                        st.markdown(f"- [{res['title']}]({res['link']})")
