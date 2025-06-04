__import__('pysqlite3')
import sys
sys.modules['sqlite3']=sys.modules.pop('pysqlite3')
import streamlit as st
import pandas as pd
from agents.eda_agent import eda_agent
from agents.dashboard_agent import dashboard_agent
from agents.preprocessing_agent import preprocessing_agent
from agents.model_suggestion_agent import model_suggestion_agent
from crewai import Task, Crew
import os

st.set_page_config(page_title="CrewAI Data Pipeline", layout="wide")
st.title("🧠 CrewAI Multi-Agent Data Pipeline")

if "results" not in st.session_state:
    st.session_state.results = {}

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"], key="csv_uploader_main")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    st.dataframe(df.head())

    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", uploaded_file.name)
    df.to_csv(csv_path, index=False)

    def get_result_text(result):
        try:
            return str(result.output)
        except AttributeError:
            return str(result)

    if st.button("Run EDA Agent"):
        csv_data = df.to_csv(index=False)
        task = Task(
            description=f"Perform EDA on the following CSV data:\n{csv_data}",
            agent=eda_agent,
            expected_output="A detailed EDA report saved to eda_report.txt."
        )
        crew = Crew(agents=[eda_agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        st.session_state.results["eda"] = result
        with open("eda_report.txt", "w", encoding="utf-8") as f:
            f.write(get_result_text(result))
        st.success("✅ EDA Agent Completed")
        st.subheader("📄 EDA Report Preview")
        st.text_area("EDA Report", value=get_result_text(result), height=400)
        st.download_button("⬇️ Download EDA Report", data=get_result_text(result), file_name="eda_report.txt")

    if st.button("Run Dashboard Agent"):
        task = Task(
            description=f"Generate visualizations for uploaded data at path: {csv_path}",
            agent=dashboard_agent,
            expected_output="Textual summary of insights and an HTML dashboard file."
        )
        crew = Crew(agents=[dashboard_agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        text_result = get_result_text(result)

        st.session_state.results["dashboard"] = text_result
        st.success("✅ Dashboard Agent Completed")

        html_path = os.path.join("dashboard_output", "insights_dashboard.html")
        if os.path.exists(html_path):
            with open(html_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Visual Insights Dashboard",
                    data=f,
                    file_name="insights_dashboard.html",
                    mime="text/html"
                )
        else:
            st.warning("⚠️ Dashboard HTML file not found.")

    if st.button("Run Preprocessing Agent"):
        task = Task(
            description=f"Run preprocessing on data at this path: {csv_path}",
            agent=preprocessing_agent,
            expected_output="Return preprocessing summary and preview of processed data."
        )
        crew = Crew(agents=[preprocessing_agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        text_result = get_result_text(result)

        st.session_state.results["preprocessing"] = text_result
        st.success("✅ Preprocessing Agent Completed")
        st.subheader("📄 Preprocessing Summary")
        st.text_area("Preprocessed Output", value=text_result, height=300)

        # Download buttons for saved files
        processed_csv = "processed_output/processed_data.csv"
        strategy_txt = "processed_output/preprocessing_strategy.txt"


        if os.path.exists(processed_csv):
            with open(processed_csv, "rb") as f:
                st.download_button(
                    "⬇️ Download Processed CSV",
                    data=f,
                    file_name="preprocessed_data.csv",
                    mime="text/csv"
                )
        if os.path.exists(strategy_txt):
            with open(strategy_txt, "rb") as f:
                st.download_button(
                    "⬇️ Download Preprocessing Strategy",
                    data=f,
                    file_name="preprocessing_strategy.txt",
                    mime="text/plain"
                )



    dataset_keywords = st.text_input("Enter dataset keywords for Kaggle/GitHub search", value="obesity prediction")

    if st.button("Run Model Suggestion Agent"):
        task = Task(
            description=f"Suggest ML models for {dataset_keywords} based on EDA, visuals, and online references.",
            agent=model_suggestion_agent,
            expected_output="Model recommendations with explanations from local and external sources."
        )
        crew = Crew(agents=[model_suggestion_agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        text_result = get_result_text(result)

        st.session_state.results["model_suggestion"] = text_result
        st.success("✅ Model Suggestion Agent Completed")
        st.subheader("🤖 Model Suggestions")
        st.text_area("Model Recommendations", value=text_result, height=300)
        st.download_button("⬇️ Download Model Suggestions", data=text_result, file_name="model_suggestions.txt")
