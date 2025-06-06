import re
import os
import random
import time
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from youtube_transcript_api import YouTubeTranscriptApi
from streamlit_lottie import st_lottie
import requests

# ------------------ Load API Key ------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ------------------ App Configuration ------------------
favicon = Image.open("assets/favicon.png")
st.set_page_config(page_title="YouTube Script Summarizer", page_icon=favicon, layout="centered")

# ------------------ Lottie Animation Loader ------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ------------------ Sidebar ------------------
with st.sidebar:
    st.image("assets/favicon.png", width=150)
    st.markdown("## 📘 Instructions")
    st.markdown("""
    1. Paste a valid YouTube video URL.  
    2. Write your instruction (e.g., "Summarize", "Extract key ideas").  
    3. Choose export format.  
    4. Click **Process** to generate output.
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ by Yasmin")

# ------------------ Header ------------------
st.markdown("""
    <h1 style='text-align: center; 
               background: -webkit-linear-gradient(90deg, #4b6cb7, #182848); 
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               font-size: 3em; 
               font-weight: bold; 
               margin-bottom: 0.5em;'>
    🎬 YouTube Video Script Summarizer
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

# ------------------ Transcript Fetcher ------------------
def validate_url(url: str) -> object:
    pattern = re.compile(
        r'^(https?://)?(www\.|m\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}(\?.*)?(&.*)?$'
    )
    if pattern.match(url):
        return url
    return {
        "status": "error",
        "message": "Invalid YouTube URL. Valid formats:\n"
                   "- https://www.youtube.com/watch?v=VIDEO_ID\n"
                   "- https://youtu.be/VIDEO_ID"
    }
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def fetch_transcript(video_url: str) -> dict:
    try:
        video_id = re.search(r'(?:v=|\/)([\w-]{11})', video_url).group(1)
        
        # Try to fetch transcript with preferred languages
        # First try Arabic, then fallback to English, then any available transcript
        preferred_langs = ['ar', 'en']

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to find transcript in preferred languages
        transcript = None
        for lang in preferred_langs:
            try:
                transcript = transcript_list.find_transcript([lang])
                break
            except NoTranscriptFound:
                continue
        
        # If still no transcript found in preferred langs, pick first available
        if not transcript:
            transcript = transcript_list.find_transcript([transcript_list._manifests[0].language_code])

        # Fetch actual transcript text
        transcript_data = transcript.fetch()

        text = " ".join([item["text"] for item in transcript_data])
        return {"status": "success", "message": text}

    except TranscriptsDisabled:
        return {"status": "error", "message": "Transcripts are disabled for this video."}
    except NoTranscriptFound:
        return {"status": "error", "message": "No transcript found in Arabic or English."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch transcript: {str(e)}"}


# ------------------ Input Form ------------------
with st.form("input_form"):
    video_url = st.text_input("📎 YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
    instruction = st.text_area("🧾 Instruction", "Summarize in 3 bullet points")
    export_format = st.selectbox("📄 Export Format", ["pdf", "word"])
    submitted = st.form_submit_button("🚀 Process")

# ------------------ Processing Logic ------------------
if submitted:
    with st.spinner("🔍 Validating YouTube URL..."):
        tip_placeholder = st.empty()
        tip_placeholder.info(get_tip())
        time.sleep(5)  # show tip for 5 seconds
        tip_placeholder.empty()  # clear tip

        validation = validate_url(video_url)
        if isinstance(validation, dict) and validation.get("status") == "error":
            st.error(validation["message"])
            st.stop()

    with st.spinner("📜 Fetching transcript..."):
        tip_placeholder = st.empty()
        tip_placeholder.info(get_tip())
        time.sleep(5)  # show tip for 5 seconds
        tip_placeholder.empty()  # clear tip

        transcript = fetch_transcript(video_url)
        message = transcript["message"]
        preview = message[:1000] + "..." if isinstance(message, str) else str(message)[:1000] + "..."
        st.success("✅ Transcript fetched successfully!")
        st.text_area("Transcript Preview", preview, height=150)


# ------------------ Footer ------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 0.9em;'>"
    "Built with <a href='https://streamlit.io' target='_blank'>Streamlit</a> | "
    "Project by Yasmin Kadry 💡"
    "</p>",
    unsafe_allow_html=True
)
