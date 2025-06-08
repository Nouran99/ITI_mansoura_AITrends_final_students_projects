# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import re
import os
import time
import random
import requests
import streamlit as st
from PIL import Image
from docx import Document
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from Crew_folder.crew import YouTubeScriptCrew


# ------------------ Load API Key ------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

# ------------------ App Configuration ------------------
favicon = Image.open("assets/favicon.png")
st.set_page_config(page_title="YouTube Script Summarizer", page_icon=favicon, layout="centered")

# ------------------ Lottie Animation Loader ------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()




# ------------------ Theme & RTL Settings ------------------
# 🌗 Theme toggle (put this before the styling block)
with st.sidebar:
    dark_mode = st.toggle("🌗 Dark Mode", value=False)

# Apply background and text colors based on theme
bg_color = "#0e1117" if dark_mode else "#ffffff"
text_color = "#ffffff" if dark_mode else "#000000"
container_color = "#1f1f1f" if dark_mode else "#f9f9f9"
primary_color = "#4b6cb7"  # You can change this for buttons if needed

# 💅 Custom CSS for form and output styling
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}

        /* ----------------- FORM STYLING ----------------- */
        .stForm {{
            background-color: {container_color};
            border-radius: 12px;
            padding: 1.5em;
            color: {text_color};
        }}

        /* Input Fields and Text Area */
        textarea, input[type="text"] {{
            background-color: {container_color} !important;
            color: {text_color} !important;
            border: 1px solid #666 !important;
            border-radius: 8px !important;
            padding: 8px !important;
        }}

        /* Selectbox Styling */
        .stSelectbox div[data-baseweb="select"] {{
            background-color: {container_color} !important;
            color: {text_color} !important;
            border-radius: 8px !important;
        }}

        /* Labels */
        label, .css-9ycgxx {{
            color: {text_color} !important;
        }}

        /* Submit Button */
        .stButton > button {{
            background-color: {primary_color};
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-weight: bold;
            border: none;
        }}

        /* RTL & LTR text direction for output */
        .rtl-text {{
            direction: rtl;
            text-align: right;
            font-family: 'Cairo', sans-serif;
        }}

        .ltr-text {{
            direction: ltr;
            text-align: left;
        }}

        /* Output Container */
        .output-container {{
            padding: 1em;
            background-color: {container_color};
            color: {text_color};
            border-radius: 12px;
            margin-top: 1em;
            margin-bottom: 1em;
            white-space: pre-wrap;
        }}
    </style>
""", unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.image("assets/favicon.png", width=150)
    st.markdown("## 📘 Instructions")
    st.markdown("""
    1. Paste a valid YouTube video URL.  
    2. Write your instruction (e.g., "Summarize", "Extract key ideas").  
    3. Choose export format.  
    4. Click **Prepare Your Script** to generate output.
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ by Yasmin")

# ------------------ Header ------------------
primary_color = "#4b6cb7"  # Gradient start
secondary_color = "#182848"  # Gradient end

st.markdown(f"""
    <h1 style='text-align: center; 
               background: -webkit-linear-gradient(90deg, {primary_color}, {secondary_color}); 
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               font-size: 3em; 
               font-weight: bold; 
               margin-bottom: 0.5em;'>
    🎬 YouTube Video Script
    </h1>
""", unsafe_allow_html=True)


# 🎞️ Lottie animation
lottie_animation = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_zrqthn6o.json")
if lottie_animation:
    st_lottie(lottie_animation, height=150, key="video-ai")

st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ Fun Tip Generator ------------------
def get_tip():
    tips = [
        "🌱 Tip: Stay curious! Learning one new tool a day builds mastery.",
        "💡 Did you know? This summarizer uses agents working together — just like a film crew!",
        "🎯 Productivity Tip: Set a timer for 25 mins and fully focus. Then take a short break!",
        "💬 Reflect: What insights are you hoping to get from this video?",
        "📘 Quick Reminder: You can export your summary as a PDF or Word file for later!",
        "🌟 Stay awesome! This app is working hard behind the scenes just for you.",
    ]
    return random.choice(tips)

# ------------------ Input Form ------------------
with st.form("input_form"):
    video_url = st.text_input("📎 YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    instruction = st.text_area("🧾 Instruction", "Get The whole Script......")
    export_format = st.selectbox("📄 Export Format", ["pdf", "word"])
    submitted = st.form_submit_button("🚀 Prepare Your Script ......🎞️")

# ------------------ Processing Logic ------------------
if submitted:
    with st.spinner("🔍 Validating YouTube URL..."):
        tip_placeholder = st.empty()
        tip_placeholder.info(get_tip())
        time.sleep(5)  # show tip for 5 seconds
        tip_placeholder.empty()  # clear tip
        st.success("✅ URL is Valid..!")

    with st.spinner("🤖 Agents are working on your Youtube Video..."):
        tip_placeholder = st.empty()
        tip_placeholder.info(get_tip())
        time.sleep(5)  # show tip for 5 seconds
        tip_placeholder.empty()  # clear tip
        try:
            crew = YouTubeScriptCrew().crew()
            inputs = {
                "video_url": video_url,
                "instruction": instruction,
                "format": export_format
            }
            result = crew.kickoff(inputs=inputs)
            tip_placeholder = st.empty()
            tip_placeholder.info(get_tip())
            time.sleep(5)  
            tip_placeholder.empty()  
            
            if not isinstance(result, str):
                result = str(result) if result is not None else ""

            # Then apply regex
            is_arabic = bool(re.search(r'[\u0600-\u06FF]', result))

            st.success("✅ Done! Here's your result:")
            st.markdown("### 📄 Result")

            # Decide on text direction class
            text_direction_class = 'rtl-text' if is_arabic else 'ltr-text'

            # Render output using safe HTML container with markdown formatting
            st.markdown(f"""
                <div class="output-container {text_direction_class}">
                    <pre>{result}</pre>
                </div>
            """, unsafe_allow_html=True)

            lottie_url_download = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
            lottie_download = load_lottieurl(lottie_url_download)     

            # with st.spinner("📦 Preparing your Script for Downloading..."):
            #     st_lottie(download_lottie, height=150, key="download-anim")
            with st_lottie_spinner(lottie_download, key="download"):
                time.sleep(5)

                from fpdf import FPDF
                import io

                if export_format == 'pdf':
                    pdf = FPDF('P', 'mm', 'A4')
                    pdf.add_page()
                    pdf.set_font('Times', size=12)

                    # Split the output text into lines and add to PDF
                    for line in result.split('\n'):
                        pdf.multi_cell(0, 10, line)

                    # Get PDF data as bytes
                    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # Latin-1 encoding for binary
                    pdf_buffer = io.BytesIO(pdf_bytes)

                    st.download_button(
                        label="⬇️ Download Script as PDF....",
                        data=pdf_buffer,
                        file_name="script.pdf",
                        mime="application/pdf"
                    )
                    
                elif export_format == 'word':
                    from docx import Document
                    import io

                    # Create Word document
                    doc = Document()
                    for line in result.split('\n'):
                        doc.add_paragraph(line)

                    # Save to a BytesIO buffer
                    word_buffer = io.BytesIO()
                    doc.save(word_buffer)
                    word_buffer.seek(0)  # Reset pointer to start

                    # Create download button
                    st.download_button(
                        label="⬇️ Download Script as Word....",
                        data=word_buffer,
                        file_name="script.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")

    st.balloons()

 ## footer   
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"""
    <p style='text-align: center; font-size: 0.9em; color: var(--text-color);'>
        Built with <a style='color: var(--primary-color); text-decoration: none;' href='https://streamlit.io' target='_blank'>Streamlit</a> | 
        Project by <a style='color: var(--primary-color); text-decoration: none;'href= 'https://www.linkedin.com/in/yasmin-kadry' arget='_blank'> | <span style="font-weight: 600;">Yasmin Kadry</span> 💡</a>
    </p>
    """,
    unsafe_allow_html=True
)

