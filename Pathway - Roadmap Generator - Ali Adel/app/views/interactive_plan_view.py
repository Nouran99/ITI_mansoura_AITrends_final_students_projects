import streamlit as st
from app.agents.agent4_json_converter import JsonConverterAgent
from app.tools.track_progress import track_progress
import os

def render_interactive_plan(plan_uploaded = False):
    # --- Step 7: Convert Plan to JSON ---
    
    if not plan_uploaded:
        if st.session_state.plan_result and not st.session_state.json_plan:
            json_converter = JsonConverterAgent(os.getenv('MODEL_NAME'))
            with st.spinner("Assembling your interactive plan..."):
                st.session_state.json_plan = json_converter.convert_plan_to_json(st.session_state.plan_result)

    # --- Step 8: Visual Plan Renderer ---
    if st.session_state.json_plan:
        st.markdown("### 🧭 Your Personalized Pathway")
        try:
            parsed_plan = st.session_state.json_plan
            if not isinstance(parsed_plan, list):
                raise ValueError("Parsed plan is not a list.")

            total_items, completed_items = track_progress(parsed_plan, st.session_state)

            # Show progress bar
            if total_items > 0:
                progress = completed_items / total_items
                st.markdown(f"#### 📈 Progress: {completed_items}/{total_items} items completed")
                st.progress(progress)

            # Display the full plan with checkbox sync
            for week_index, week in enumerate(parsed_plan):
                week_num = week.get("week_number", f"{week_index+1}")
                with st.expander(f"📅 Week {week_num}", expanded=False):
                    
                    st.markdown(f"#### 🎯 Objective: {week.get('objective', 'No objective')}\n")

                    # --- Topics ---
                    st.markdown("##### 📘 Topics to Study")
                    for topic_index, topic_dict in enumerate(week.get("topics", [])):
                        topic_name = topic_dict.get("name", f"Unnamed Topic {topic_index+1}")
                        key = f"w{week_num}_topic_{topic_index}"
                        checked = st.checkbox(topic_name, key=key, value=topic_dict.get("completed", False))
                        topic_dict["completed"] = checked  # Update the state in the dict

                    # --- Tasks ---
                    st.markdown("##### 🛠️ Practice Tasks")
                    for task_index, task_dict in enumerate(week.get("tasks", [])):
                        task_desc = task_dict.get("description", f"Unnamed Task {task_index+1}")
                        key = f"w{week_num}_task_{task_index}"
                        checked = st.checkbox(task_desc, key=key, value=task_dict.get("completed", False))
                        task_dict["completed"] = checked  # Update the state in the dict

            # Reflect updated progress in session state
            st.session_state.json_plan = parsed_plan
                
        except Exception as e:
            st.error("⚠️ Something went wrong while displaying your plan.")
            st.markdown("Please review the plain text version or regenerate if needed.")
            st.code(str(e))
    elif st.session_state.plan_result:
        st.warning("⚠️ Interactive plan is not avalible at the moment.")
        st.markdown("Please review the plain text version or regenerate if needed.")