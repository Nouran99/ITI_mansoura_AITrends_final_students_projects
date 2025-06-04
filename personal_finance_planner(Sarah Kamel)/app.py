import streamlit as st
from agents.advice_agent import AdviceAgent
from agents.analysis_agent import AnalysisAgent
from agents.data_processing_agent import DataProcessingAgent
from utils.llm_model import LLMModel
import tempfile

st.set_page_config(page_title="Personal Finance Planner", layout="centered")

st.title("💰 Personal Finance Planner")

uploaded_file = st.file_uploader("📂 upload finance file (CSV, Excel, أو TXT):", type=["csv", "xlsx", "xls", "txt"])

if uploaded_file:

    llm = LLMModel()
    data_agent = DataProcessingAgent()
    analysis_agent = AnalysisAgent(llm)
    advice_agent = AdviceAgent(llm)


    df_or_text = data_agent.read_file(uploaded_file)

    if isinstance(df_or_text, str) and "Unsupported file type" in df_or_text:
        st.error(df_or_text)
    else:
        st.success("✅file uploaded ")
        if isinstance(df_or_text, str):
            st.text_area("📄 file content :", df_or_text, height=300)
        else:
            st.dataframe(df_or_text)

        user_prompt = data_agent.convert_data_to_prompt(df_or_text)

        if st.button("🔍 Data analysis and advice generation"):
            with st.spinner("📊 Data analysis and advice generation ..."):
                try:
                    analysis = analysis_agent.analyze(user_prompt)
                    st.subheader("📈 Financial analysis:")
                    st.text_area("result:", analysis, height=250)

                    advice, report_path = advice_agent.run(analysis)
                    st.subheader("💡 Tips and recommendations:")
                    st.text_area("Tips:", advice, height=250)

                    with open(report_path, "rb") as f:
                        st.download_button("📥 Download the text report", f, file_name="financial_advice_report.txt")
                except Exception as e:
                    st.error(f"❌ An error occurred during analysis or generation:\n{str(e)}")
