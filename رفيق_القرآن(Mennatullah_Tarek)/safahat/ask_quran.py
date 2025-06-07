import streamlit as st
import json
import re
import os
from transformers import pipeline
import nest_asyncio

nest_asyncio.apply()

# ========================
# CONFIGURATION
# ========================

PRIMARY_COLOR = "#2E7D32"
ACCENT_COLOR = "#FFC107"
BACKGROUND_COLOR = "#fffbf2"

# ========================
# ENVIRONMENT & DATA LOADING
# ========================
@st.cache_resource
def load_surah_data(filepath="surah_info.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

class QuranData:
    def __init__(self, filepath="surah_info.json"):
        self.filepath = filepath
        self.data = load_surah_data(self.filepath)

# ========================
# TOOLS & MODEL WRAPPER
# ========================
@st.cache_resource
def load_llm_model():
    with st.spinner("⏳ جاري تحميل نموذج اللغة... يرجى الانتظار"):
        return pipeline("question-answering", model="Damith/AraELECTRA-discriminator-QuranQA")

class QuranQATools:
    def __init__(self):
        self.llm = load_llm_model()

    @staticmethod
    def extract_surah_name(question):
        match = re.search(r"سورة\s+([\w]+)", question)
        return match.group(1) if match else None

    def get_context(self, surah_name, surah_data):
        for surah in surah_data:
            if surah_name == surah["name_ar"]:
                return (
                    f"سورة {surah['name_ar']} هي سورة {surah['revelation_place']}، "
                    f"عدد آياتها {surah['verses_count']}، "
                    f"نزلت في {surah['revelation_time']}، "
                    f"والهدف منها: {surah['reasons']}."
                )
        return ""

    def generate_answer(self, question, context):
        if not context:
            return "لا توجد معلومات كافية للإجابة على هذا السؤال."
        result = self.llm(question=question, context=context)
        return result["answer"]

# ========================
# AGENT
# ========================
class QuranAgent:
    def __init__(self, data: QuranData, tools: QuranQATools):
        self.data = data
        self.tools = tools

    def is_greeting(self, question):
        greetings = {
            "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته 🌸",
            "مرحبا": "مرحبًا بك يا رفيق! 😊 كيف يمكنني مساعدتك في تدبر السور؟",
            "من أنت": "أنا مساعد ذكي لتدبر سور القرآن الكريم ✨ اسألني عن أي سورة وسأساعدك.",
            "أهلا": "أهلاً وسهلاً بك! 🌟 كيف يمكنني خدمتك؟",
            "😊 شكر" : " على الرحب. تسرني مساعدتك"
        }
        q_clean = question.strip().lower().replace("؟", "").replace("!", "")
        for key in greetings:
            if key in q_clean:
                return greetings[key]
        return None

    def answer_question(self, question):
        greeting_response = self.is_greeting(question)
        if greeting_response:
            return greeting_response

        surah_name = self.tools.extract_surah_name(question)
        if not surah_name:
            return "❗ يرجى ذكر اسم السورة في سؤالك. مثل: ما هدف سورة البقرة؟"

        context = self.tools.get_context(surah_name, self.data.data)
        answer = self.tools.generate_answer(question, context)
        return f"{answer}"

# ========================
# UI
# ========================
def render_message(user_msg, bot_msg):
    st.markdown(
        f"""
        <style>
        .chat-container {{
            max-width: 700px;
            margin: 0 auto 10px auto;
            font-family:  'Cairo', sans-serif;
            background-color: {BACKGROUND_COLOR};
            padding: 10px 20px;
            border-radius: 12px;
        }}
        .message {{
            display: flex;
            margin-bottom: 12px;
            align-items: flex-start;
        }}
        .user-msg {{
            justify-content: flex-start;
        }}
        .bot-msg {{
            justify-content: flex-end;
        }}
        .bubble {{
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            font-size: 16px;
            line-height: 1.4;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .user-bubble {{
            background-color: #DCF8C6;
            color: #000;
            border-bottom-left-radius: 0;
        }}
        .bot-bubble {{
            background-color: {ACCENT_COLOR};
            color: #000;
            border-bottom-right-radius: 0;
        }}
        .user-icon {{
            font-weight: bold;
            margin-right: 10px;
            color: {PRIMARY_COLOR};
            min-width: 30px;
            text-align: center;
        }}
        .bot-icon {{
            font-weight: bold;
            margin-left: 10px;
            color: #5a4b00;
            min-width: 30px;
            text-align: center;
        }}


        </style>

        <div class="chat-container">
            <div class="message user-msg">
                <div class="user-icon">👤</div>
                <div class="bubble user-bubble">{user_msg}</div>
            </div>
            <div class="message bot-msg">
                <div class="bubble bot-bubble">🤖 {bot_msg}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display_ui(agent: QuranAgent):
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {BACKGROUND_COLOR};
            direction: rtl;
            font-family: 'Cairo', sans-serif;
        }}
        .main-title {{
            color: {PRIMARY_COLOR};
            font-size: 2.2rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #555;
            font-size: 1rem;
            margin-bottom: 20px;
        }}
        button[kind="PRIMARY_COLOR"] {{
            background-color: #2E7D32 !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: bold !important;
            border: none !important;
            padding: 0.5rem 1.2rem !important;
        }}
    
        .stButton>button {{
            background-color: #388E3C;
            color: white;
            font-size: 1rem;
            border-radius: 8px;
            padding: 0.4rem 1rem;
            margin-top: 10px;
            border: 2px solid #2E7D32;
            transition: all 0.3s ease;
        }}
    
        .stButton>button:hover {{
            background-color: #1B5E20;
            border-color: #1B5E20;
            transform: scale(1.03);
        }}

                .stForm button {{
        background-color: #388E3C;
        color: white;
        font-size: 1rem;
        border-radius: 8px;
        padding: 0.4rem 1rem;
        margin-top: 10px;
        border: 2px solid #2E7D32;
        transition: all 0.3s ease;
        font-weight: bold;
        cursor: pointer;
    }}

    .stForm button:hover {{
        background-color: #1B5E20;
        border-color: #1B5E20;
        transform: scale(1.03);
    }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🤖 مساعد تدبر السور القرآنية</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">اكتب سؤالك متضمنًا اسم السورة وسيتم استخراج الإجابة ✨</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("✍️ اكتب سؤالك هنا", key="input")
        submitted = st.form_submit_button("🔍 إرسال")

    if submitted and user_input.strip():
        response = agent.answer_question(user_input)
        st.session_state.chat_history.append((user_input, response))

    for user_msg, bot_msg in st.session_state.chat_history[::]: 
        render_message(user_msg, bot_msg)

# ========================
# MAIN APP
# ========================
def app():
    data = QuranData()
    tools = QuranQATools()
    agent = QuranAgent(data, tools)
    display_ui(agent)

if __name__ == "__main__":
    app()
