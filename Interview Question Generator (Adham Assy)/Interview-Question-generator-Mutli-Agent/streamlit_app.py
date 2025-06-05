__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import os
import sys
import tempfile
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DEFAULT_HF_TOKEN = os.getenv("HF_TOKEN")

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

# Local utility imports (safe)
from tools.pdf_parser_tool import PDFParserTool
from utils.pdf_exporter import export_to_pdf

# Delay agent setup to avoid slow startup
def get_interview_runner():
    from crew.mycrew import run_interview_process
    return run_interview_process

# PDF extraction logic
def extract_text_from_pdf(file_path):
    parser = PDFParserTool()
    return parser._run(file_path=file_path)

# UI layout
st.set_page_config(page_title="AI Interview Generator", layout="wide")
st.title("🎯 Custom Interview Question Generator")

# Sidebar: Hugging Face token input
with st.sidebar:
    st.markdown("### 🔑 Hugging Face Token (optional)")
    user_token = st.text_input("Enter your token", type="password", placeholder="hf_...")
    effective_token = user_token.strip() or DEFAULT_HF_TOKEN
    if not effective_token:
        st.warning("⚠️ No Hugging Face token set. Please add one to use the app.")

# User input section
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📄 Upload CV (PDF)", type="pdf")
with col2:
    job_title = st.text_input("🧑‍💻 Job Title", placeholder="e.g., AI Engineer")
    job_description = st.text_area("📋 Job Description (optional)")

# Generate questions on click
if st.button("🚀 Generate Interview Questions"):
    if not uploaded_file or not job_title:
        st.error("❗ Please upload a CV and enter a job title.")
        st.stop()

    with st.spinner("📄 Reading CV..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                pdf_path = tmp.name

            cv_text = extract_text_from_pdf(pdf_path)
            os.remove(pdf_path)
        except Exception as e:
            st.error(f"❌ Error extracting PDF text: {e}")
            st.stop()

    if len(cv_text.strip()) < 50:
        st.error("❌ Extracted CV text is too short.")
        st.stop()

    # Show progress bar instead of spinner
    progress_bar = st.progress(0, text="🧠 Generating questions...")
    
    # Simulate incremental steps to show activity (not required, but improves UX)
    for percent_complete in range(0, 70, 10):
        import time
        time.sleep(0.3)
        progress_bar.progress(percent_complete, text="🧠 Generating questions...")
    
    try:
        run_interview = get_interview_runner()
        questions = run_interview(cv_text, job_title, job_description, hf_token=effective_token)
    
        # Complete the progress bar after successful generation
        progress_bar.progress(100, text="✅ Questions generated!")
    
    except Exception as e:
        progress_bar.empty()
        st.error(f"❌ Agent execution failed: {e}")
        st.stop()


    if not questions or not isinstance(questions, list):
        st.error("⚠️ No questions generated.")
        st.stop()

    # Show results
    st.success("✅ Questions generated!")
    st.subheader("📋 Interview Questions")
    for i, q in enumerate(questions, 1):
        if isinstance(q, dict):
            st.markdown(f"**Q{i}.** {q.get('question', 'Unknown')} ({q.get('category', 'General')})")
        else:
            st.markdown(f"**Q{i}.** {q}")

    # PDF export
    try:
        pdf_data = export_to_pdf(questions)
        st.download_button("📄 Download PDF", data=pdf_data, file_name="interview_questions.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"PDF generation failed: {e}")

    # JSON export
    try:
        import json
        json_data = json.dumps({"questions": questions}, indent=2)
        st.download_button("📊 Download JSON", data=json_data, file_name="interview_questions.json", mime="application/json")
    except Exception as e:
        st.error(f"JSON export failed: {e}")

# App info
with st.expander("ℹ️ How this works"):
    st.markdown("""
    This app uses AI agents to generate technical interview questions based on your uploaded CV and a given job title. If you run out of free usage on our Hugging Face API key, add your own token in the sidebar.

    **Steps:**
    1. Upload your resume as PDF.
    2. Enter the job title (and optionally description).
    3. Click "Generate".
    4. Download the questions as PDF or JSON.
    """)
