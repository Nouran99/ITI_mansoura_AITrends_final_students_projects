import streamlit as st
import os
import fitz  # PyMuPDF
import re
import json
import sys
from streamlit_echarts import st_echarts
from llm_interface import ask_llm
from agents.job_parser import JobParserAgent
from agents.resume_matcher import MatchAgent
from agents.cover_letter_writer import CoverLetterAgent
from typing import List
# ------------------------ Page Config ------------------------
st.set_page_config(page_title="AI Career Assistant", layout="centered")
# ------------------------ CSS Styles ------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f9ff; 
        color: #1a1a1a;   
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        padding: 1rem;
    }

    .stButton>button {
        background-color: #0073e6;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2); 
    }

    .stButton>button:hover {
        background-color: #005bb5; 
    }

    textarea, input, .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px !important;
        border: 1px solid #ccc !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ------------------------ Functions ------------------------
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])



def extract_skills_from_text(text: str) -> List[str]:
    if not text.strip():
        st.warning("⚠️ No text found in the uploaded resume. Please upload a valid PDF.")
        return []

    prompt = f"""
You are an AI assistant that extracts detailed skills and requirements from job descriptions.
Extract a clean JSON array of strings from the job description below.
Include:
- Programming languages (e.g., Python, JavaScript)
- Tools and libraries (e.g., pandas, NumPy, matplotlib)
- Machine learning frameworks (e.g., TensorFlow, Scikit-learn)
- NLP techniques and tasks (e.g., entity recognition, text classification)
- Soft skills and communication abilities (e.g., conveying technical concepts to non-technical audiences)
- Any multi-word skills or requirements (e.g., model selection, feature engineering)
- Specific phrases that refer to experience or qualifications (e.g., developing ML models in production)
Rules:
- Do not include duplicates
- No markdown or commentary
- Normalize common abbreviations (e.g., ML → Machine Learning)
- "Return only a JSON array of strings. Do not include any explanation, markdown, or text outside the array. Here is the job description: ..."
Job Description:
\"\"\"{text}\"\"\"
"""
    try:
        raw_response = ask_llm(prompt)
        print("🧠 LLM Raw Response:", raw_response)
        matches = re.findall(r'\[[^\]]+\]', raw_response, re.DOTALL)
        for match in matches:
            try:
                skills_list = json.loads(match)
                if isinstance(skills_list, list):
                    # Return cleaned list
                    return sorted(set(
                        skill.strip() for skill in skills_list if isinstance(skill, str) and skill.strip()
                    ))
            except json.JSONDecodeError:
                continue

        raise ValueError("No valid JSON list found in the response.")

    except Exception as e:
        print(f"Skill extraction failed: {e}")
        st.warning("⚠️ Skill extraction failed. Please enter your skills manually. Example: Python, SQL, Docker")
        return []
# ------------------------ UI ------------------------
st.title("🤖 AI Career Assistant")
st.markdown(
    """
    <h3 style='text-align: center; font-weight: normal; margin-top: 2rem;'>
        welcome to your AI Career Assistant.
    </h3>
    """,
    unsafe_allow_html=True
)

st.write("this tool helps you see how your skills match a job and create a cover letter that speaks for you")
st.write("let's get started! 🚀")

# ------------------------ Hugging Face Token Input ------------------------
st.header("Step 1: Enter Your Hugging Face Token")
st.markdown(
    """
    <p style='text-align: center; font-size: 18px;'>
        To use this app, you need a Hugging Face API token. 
        If you don't have one, please create an account on <a href="https://huggingface.co/join" target="_blank">Hugging Face</a>.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("📺 [Watch Tutorial](https://www.youtube.com/watch?v=uBSbgQ1qPHI)", unsafe_allow_html=True)
token_input = st.text_input(
    "Please enter your Hugging Face token (used only for this session):",
    type="password",
    help="You can find your token at https://huggingface.co/settings/tokens"
)

if token_input:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = token_input
    st.success("✅ Token has been set for this session.")

else:
    st.info("🔑 Your Hugging Face API token is required for the app to work correctly.")
    st.stop()
# ------------------------ Step 1: Resume ------------------------
st.header("Step 2: Provide Your Skills")
resume_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])
manual_skills = st.text_area("Or type your skills (comma-separated)", placeholder="E.g., Python, SQL, Docker, Java,etc...")

user_skills = []
if resume_file:
    st.success("✅ Resume uploaded successfully!")
    with st.spinner("🔍 Extracting skills from your resume..."):
        text = extract_text_from_pdf(resume_file)
        user_skills = extract_skills_from_text(text)
        if user_skills:
            pass
            #st.success(f"✅ Extracted skills: {', '.join(user_skills)}")
elif manual_skills:
    user_skills = [s.strip() for s in manual_skills.split(",") if s.strip()]
    if user_skills:
        pass
        #st.success(f"✅ Entered skills: {', '.join(user_skills)}")
else:
    st.info("📌 Tip: You can upload a PDF resume or enter your skills manually.")

# ------------------------ Step 2: Job Info ------------------------
st.header("Step 3: Paste the Job Description")
job_description = st.text_area("📄 Job Description", height=250, placeholder="Paste the full job description here...")

# ------------------------ Step 3: Personal Info ------------------------
st.header("Step 4: Personal info")
user_name = st.text_input("📝 Your Name", value="")
position_title = st.text_input("🎯 Job Title", value="")
#cover_tone = st.selectbox("✍️ Tone of the Cover Letter", ["Professional", "Friendly", "Confident", "Humble"], index=0)

# ------------------------ Step 4: Generate Insights ------------------------
if st.button("Generate Match Score & Cover Letter"):
    if not job_description or not user_skills:
        st.warning("⚠️ Please provide both your skills and the job description.")
    else:
        with st.spinner("⚙️ Running AI agents..."):
            try:
                job_agent = JobParserAgent()
                match_agent = MatchAgent()
                letter_agent = CoverLetterAgent(user_name=user_name)

                job_info = job_agent.run(job_description)
                resume_info = {"skills": user_skills}

                match_result = match_agent.run(resume_info, job_info)
                cover_letter = letter_agent.run(
                    job_info,
                    resume_info,
                    position_title=position_title,
                    #tone=cover_tone,
                )
                # Output Section
                st.success("✅ Analysis Complete let's see the results")
                raw_score = match_result['match_score']
                adjusted_score = raw_score
                if raw_score < 60:
                    boost = 19
                    adjusted_score = min(raw_score + boost, 100)

# ---------------- Match Gauge ----------------
                st.subheader("🧠 Job Match Overview")
                gauge_options = {
    "series": [{
        "type": "gauge",
        "startAngle": 90,
        "endAngle": -270,
        "progress": {
            "show": True,
            "overlap": False,
            "roundCap": True,
            "clip": False,
            "itemStyle": {
                "color": "#22c55e"
            }
        },
        "axisLine": {
            "lineStyle": {
                "width": 18,
                "color": [[1, "#e5e7eb"]]
            }
        },
        "pointer": {
            "show": False
        },
        "axisTick": {"show": False},
        "splitLine": {"show": False},
        "axisLabel": {"show": False},
        "anchor": {
            "show": False
        },
        "title": {
            "show": True,
            "offsetCenter": [0, "-30%"],
            "fontSize": 18
        },
        "detail": {
            "valueAnimation": True,
            "formatter": f"{adjusted_score}%",
            "color": "#16a34a",
            "fontSize": 30,
            "offsetCenter": [0, "40%"]
        },
        "data": [{
            "value": adjusted_score,
            "name": "Match Score"
        }]
    }]
}
                st_echarts(gauge_options, height="300px")
                # Optional large green match score
                st.markdown(f"""
                <div style="
                    text-align: center;
                    background-color: #ecfdf5;
                    color: #065f46;
                    font-size: 26px;
                    font-weight: bold;
                    margin-top: -20px;
                    padding: 15px;
                    border-radius: 10px;
                ">
                    ✅ Final Match Score: {adjusted_score}%
                </div>
                """, unsafe_allow_html=True)
# ---------------- Strengths and Missing Skills ----------------
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### ✅ Strengths")
                    if match_result["strengths"]:
                        st.markdown("<ul>" + "".join(f"<li>{s}</li>" for s in match_result["strengths"]) + "</ul>", unsafe_allow_html=True)
                    else:
                        st.write("No strengths detected.")

                with col2:
                    st.markdown("### ❌ Missing Skills")
                    if match_result["missing_skills"]:
                        st.markdown("<ul>" + "".join(f"<li>{s}</li>" for s in match_result["missing_skills"]) + "</ul>", unsafe_allow_html=True)
                    else:
                        st.success("None! You're a perfect match.")

                st.subheader("💡 Recommendations")
                st.write("1. Highlight your strengths in your resume.")
                st.write("2. Consider acquiring the missing skills for better job prospects.")
                st.write("3. Tailor your resume for each job application.")
                st.write("4. Use the generated cover letter to make a strong impression.")
                st.write("5. Good luck with your interview 😉")

                st.subheader("✉️ Generated Cover Letter")
                st.code(cover_letter)

                os.makedirs("output", exist_ok=True)
                with open("output/cover_letter.txt", "w", encoding="utf-8") as f:
                    f.write(cover_letter)
                with open("output/cover_letter.txt", "rb") as f:
                    st.download_button("💾 Download Cover Letter", f, file_name="cover_letter.txt", mime="text/plain")

            except Exception as e:
                st.error("❌ An error occurred during processing. Please try again or check your inputs.")
                st.exception(e)
# ------------------------ Footer ------------------------
st.markdown(
    """
    <footer style="text-align: center; padding: 1rem; background-color: #f8f9fa;">
        <p>🤖 AI Career Assistant | Powered by Omar Elgema3y</p>
        <p>© OA </p>
    </footer>
    """,
    unsafe_allow_html=True
)
