import streamlit as st
import pandas as pd
import os
import datetime
import requests



class HifzEnvironment:
    def __init__(self, log_file="data/hifz_log.csv"):
        self.log_file = log_file
        os.makedirs("data", exist_ok=True)

    def save_record(self, surah, aya):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {"سورة": surah, "آية": aya, "الوقت": now}
        df = self.load_log()
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.log_file, index=False)

    def load_log(self):
        if os.path.exists(self.log_file):
            return pd.read_csv(self.log_file)
        else:
            return pd.DataFrame(columns=["سورة", "آية", "الوقت"])



class QuranAPI:
    @staticmethod
    def get_audio_url(sura, aya):
        try:
            response = requests.get(f"https://api.alquran.cloud/v1/ayah/{sura}:{aya}/ar.alafasy")
            if response.status_code == 200:
                return response.json()["data"]["audio"]
            else:
                return None
        except Exception:
            return None



class HifzAgent:
    def __init__(self, environment, tools):
        self.env = environment
        self.tools = tools

    def play_ayah(self, surah_name, surah_number, aya_number, repeat=False):
        audio_url = self.tools.get_audio_url(surah_number, aya_number)
        if audio_url:
            st.audio(audio_url, format="audio/mp3")
            if repeat:
                st.info("🔄 تم تكرار الآية.")
            else:
                st.success("✅ تم تشغيل الآية.")
            self.env.save_record(surah_name, aya_number)
        else:
            st.error("⚠️ لم يتم العثور على رابط الصوت.")

    def show_log(self):
        with st.expander("📜 عرض سجل الاستماع"):
            df = self.env.load_log()
            if df.empty:
                st.info("لا يوجد سجل محفوظ بعد.")
            else:
                st.dataframe(df.tail(10), use_container_width=True)



def display_ui(agent):
   
    st.markdown("""
    <style>
    body, .stApp {
        background-color: #fffbf2;
        direction: rtl;
        font-family: 'Cairo', sans-serif;
    }
    .main-title {
        color: #2E7D32;
        font-size: 2.3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    button[kind="primary"] {
        background-color: #2E7D32 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 1.2rem !important;
    }

    .stButton>button {
        background-color: #388E3C;
        color: white;
        font-size: 1rem;
        border-radius: 8px;
        padding: 0.4rem 1rem;
        margin-top: 10px;
        border: 2px solid #2E7D32;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1B5E20;
        border-color: #1B5E20;
        transform: scale(1.03);
    }

    </style>
""", unsafe_allow_html=True)


    st.markdown('<div class="main-title">🎧 مساعد الحفظ الذكي</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">اختر السورة والآية واستمع إليها وكررها بسهولة ✨</div>', unsafe_allow_html=True)

 
    surah_list = [
        ("الفاتحة", 1), ("البقرة", 2), ("آل عمران", 3), ("النساء", 4), ("المائدة", 5),
        ("الأنعام", 6), ("الأعراف", 7), ("الأنفال", 8), ("التوبة", 9), ("يونس", 10),
        ("هود", 11), ("يوسف", 12), ("الرعد", 13), ("إبراهيم", 14), ("الحجر", 15),
        ("النحل", 16), ("الإسراء", 17), ("الكهف", 18), ("مريم", 19), ("طه", 20),
        ("الأنبياء", 21), ("الحج", 22), ("المؤمنون", 23), ("النّور", 24), ("الفرقان", 25),
        ("الشعراء", 26), ("النمل", 27), ("القصص", 28), ("العنكبوت", 29), ("الروم", 30),
        ("لقمان", 31), ("السجدة", 32), ("الأحزاب", 33), ("سبأ", 34), ("فاطر", 35),
        ("يس", 36), ("الصافات", 37), ("ص", 38), ("الزمر", 39), ("غافر", 40),
        ("فصلت", 41), ("الشورى", 42), ("الزخرف", 43), ("الدخان", 44), ("الجاثية", 45),
        ("الأحقاف", 46), ("محمد", 47), ("الفتح", 48), ("الحجرات", 49), ("ق", 50),
        ("الذاريات", 51), ("الطور", 52), ("النجم", 53), ("القمر", 54), ("الرحمن", 55),
        ("الواقعة", 56), ("الحديد", 57), ("المجادلة", 58), ("الحشر", 59), ("الممتحنة", 60),
        ("الصف", 61), ("الجمعة", 62), ("المنافقون", 63), ("التغابن", 64), ("الطلاق", 65),
        ("التحريم", 66), ("الملك", 67), ("القلم", 68), ("الحاقة", 69), ("المعارج", 70),
        ("نوح", 71), ("الجن", 72), ("المزّمّل", 73), ("المدّثر", 74), ("القيامة", 75),
        ("الإنسان", 76), ("المرسلات", 77), ("النبأ", 78), ("النازعات", 79), ("عبس", 80),
        ("التكوير", 81), ("الإنفطار", 82), ("المطفّفين", 83), ("الإنشقاق", 84), ("البروج", 85),
        ("الطارق", 86), ("الأعلى", 87), ("الغاشية", 88), ("الفجر", 89), ("البلد", 90),
        ("الشمس", 91), ("الليل", 92), ("الضحى", 93), ("الشرح", 94), ("التين", 95),
        ("العلق", 96), ("القدر", 97), ("البينة", 98), ("الزلزلة", 99), ("العاديات", 100),
        ("القارعة", 101), ("التكاثر", 102), ("العصر", 103), ("الهمزة", 104), ("الفيل", 105),
        ("قريش", 106), ("الماعون", 107), ("الكوثر", 108), ("الكافرون", 109), ("النصر", 110),
        ("المسد", 111), ("الإخلاص", 112), ("الفلق", 113), ("الناس", 114)
    ]

    surah_name = st.selectbox("📘 اختر السورة", [name for name, _ in surah_list])
    surah_number = next(num for name, num in surah_list if name == surah_name)
    aya_number = st.number_input("🔢 رقم الآية", min_value=1, step=1)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ تشغيل الآية"):
            agent.play_ayah(surah_name, surah_number, aya_number)
    with col2:
        if st.button("🔁 كرر الآية مرة أخرى"):
            agent.play_ayah(surah_name, surah_number, aya_number, repeat=True)

    agent.show_log()



def app():
    env = HifzEnvironment()
    tools = QuranAPI()
    agent = HifzAgent(env, tools)
    display_ui(agent)

if __name__ == "__main__":
    app()
