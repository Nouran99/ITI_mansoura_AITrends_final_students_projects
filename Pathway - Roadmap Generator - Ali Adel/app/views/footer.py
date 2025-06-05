import streamlit as st
import json
from app.tools.generate_pdf import export_pdf

def render_footer():
    has_pdf = bool(st.session_state.get("plan_result"))
    has_json = bool(st.session_state.get("json_plan"))

    if has_pdf and has_json:
        col1, col2 = st.columns(2)
        with col1:
            pdf = export_pdf(st.session_state.plan_result)
            st.download_button(
                label="📥 Download Plan as PDF",
                data=pdf,
                file_name=f"{st.session_state.learning_goal}_learning_plan.pdf",
                mime="application/pdf"
            )
        with col2:
            json_data = json.dumps(st.session_state.json_plan, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download Plan as JSON",
                data=json_data,
                file_name=f"{st.session_state.learning_goal}_learning_plan.json",
                mime="application/json"
            )

    elif has_pdf:
        pdf = export_pdf(st.session_state.plan_result)
        st.download_button(
            label="📥 Download Plan as PDF",
            data=pdf,
            file_name=f"{st.session_state.learning_goal}_learning_plan.pdf",
            mime="application/pdf"
        )

    elif has_json:
        json_data = json.dumps(st.session_state.json_plan, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download Plan as JSON",
            data=json_data,
            file_name=f"{st.session_state.learning_goal}_learning_plan.json",
            mime="application/json"
        )
