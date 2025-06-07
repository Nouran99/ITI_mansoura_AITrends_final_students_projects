import nest_asyncio
nest_asyncio.apply()

import streamlit as st
import requests
import difflib
import re
import csv
from io import StringIO


def apply_custom_styles():
    st.markdown("""
        <style>
        body {
            font-family: 'Cairo', sans-serif;
            direction: rtl;
        }

        .stApp {
            background-color: #f9f9f9;
            padding: 20px;
        }

        .title {
            color: #2e7d32;
            text-align: center;
            margin-bottom: 30px;
        }

        .stButton button {
            background-color: #4caf50 !important;
            color: white !important;
            font-weight: bold;
        }

        .score-box {
            padding: 0.5rem;
            border-radius: 6px;
            font-weight: bold;
            text-align: center;
            margin-top: 0.5rem;
            font-size: 1rem;
        }

        .score-good {
            background-color: #c8e6c9;
            color: #1b5e20;
        }

        .score-average {
            background-color: #fff9c4;
            color: #f57f17;
        }

        .score-poor {
            background-color: #ffcdd2;
            color: #c62828;
        }

        .stars {
            font-size: 1.2rem;
            color: #fbc02d;
            margin-top: 0.3rem;
        }

        textarea {
            border-radius: 10px !important;
            padding: 10px !important;
        }

        .stDownloadButton button {
            background-color: #4caf50 !important;
            color: white !important;
            font-weight: bold;
        }

        hr {
            border: none;
            height: 1px;
            background-color: #ddd;
            margin: 25px 0;
        }
        </style>
    """, unsafe_allow_html=True)


def render_score_visual(score):
    try:
        score = float(score)
    except:
        return ""

    if score >= 85:
        css_class = "score-good"
        stars = "⭐⭐⭐⭐⭐"
    elif score >= 60:
        css_class = "score-average"
        stars = "⭐⭐⭐☆☆"
    else:
        css_class = "score-poor"
        stars = "⭐☆☆☆☆"

    return f"""
        <div class="score-box {css_class}">
            التقييم البصري: {score}%
            <div class="stars">{stars}</div>
        </div>
    """


class TextProcessor:
    @staticmethod
    def strip_tashkeel(text):
        return re.sub(r'[\u064B-\u0652]', '', text)

    @staticmethod
    def compare_ayah(user_input, actual_text):
        actual_clean = TextProcessor.strip_tashkeel(actual_text.replace('\n', '').strip())
        user_clean = TextProcessor.strip_tashkeel(user_input.replace('\n', '').strip())
        similarity_ratio = difflib.SequenceMatcher(None, actual_clean, user_clean).ratio()
        return round(similarity_ratio * 100, 2)

# --- Agent: Ayah Fetcher ---
class AyahFetcher:
    @staticmethod
    def get_ayah_text(surah_id, ayah_number):
        url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_id}:{ayah_number}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['verses'][0]['text_uthmani']
            except (KeyError, IndexError):
                return "⚠️ لم يتم العثور على نص الآية."
        return "❌ فشل الاتصال بجلب الآية."


class TafsirFetcher:
    @staticmethod
    def get_tafsir(surah_id, ayah_number, tafsir_id=91):
        url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_id}:{ayah_number}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['tafsir']['text']
            except (KeyError, TypeError):
                return "⚠️ لم يتم العثور على التفسير."
        return "❌ فشل الاتصال بجلب التفسير."


def get_surahs():
    return {
        "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5,
        "الأنعام": 6, "الأعراف": 7, "الأنفال": 8, "التوبة": 9, "يونس": 10,
        "هود": 11, "يوسف": 12, "الرعد": 13, "إبراهيم": 14, "الحجر": 15,
        "النحل": 16, "الإسراء": 17, "الكهف": 18, "مريم": 19, "طه": 20,
        "الأنبياء": 21, "الحج": 22, "المؤمنون": 23, "النور": 24, "الفرقان": 25,
        "الشعراء": 26, "النمل": 27, "القصص": 28, "العنكبوت": 29, "الروم": 30,
        "لقمان": 31, "السجدة": 32, "الأحزاب": 33, "سبأ": 34, "فاطر": 35,
        "يس": 36, "الصافات": 37, "ص": 38, "الزمر": 39, "غافر": 40,
        "فصلت": 41, "الشورى": 42, "الزخرف": 43, "الدخان": 44, "الجاثية": 45,
        "الأحقاف": 46, "محمد": 47, "الفتح": 48, "الحجرات": 49, "ق": 50,
        "الذاريات": 51, "الطور": 52, "النجم": 53, "القمر": 54, "الرحمن": 55,
        "الواقعة": 56, "الحديد": 57, "المجادلة": 58, "الحشر": 59, "الممتحنة": 60,
        "الصف": 61, "الجمعة": 62, "المنافقون": 63, "التغابن": 64, "الطلاق": 65,
        "التحريم": 66, "الملك": 67, "القلم": 68, "الحاقة": 69, "المعارج": 70,
        "نوح": 71, "الجن": 72, "المزّمّل": 73, "المدّثر": 74, "القيامة": 75,
        "الإنسان": 76, "المرسلات": 77, "النبأ": 78, "النازعات": 79, "عبس": 80,
        "التكوير": 81, "الإنفطار": 82, "المطفّفين": 83, "الإنشقاق": 84, "البروج": 85,
        "الطارق": 86, "الأعلى": 87, "الغاشية": 88, "الفجر": 89, "البلد": 90,
        "الشمس": 91, "الليل": 92, "الضحى": 93, "الشرح": 94, "التين": 95,
        "العلق": 96, "القدر": 97, "البينة": 98, "الزلزلة": 99, "العاديات": 100,
        "القارعة": 101, "التكاثر": 102, "العصر": 103, "الهمزة": 104, "الفيل": 105,
        "قريش": 106, "الماعون": 107, "الكوثر": 108, "الكافرون": 109, "النصر": 110,
        "المسد": 111, "الإخلاص": 112, "الفلق": 113, "الناس": 114
    }


def simple_tafsir_evaluation(user_tafsir, actual_tafsir):
    if not user_tafsir.strip():
        return "❌ لم تقم بإدخال تفسير."
    elif len(user_tafsir.strip().split()) < 5:
        return "🔸 التفسير قصير جدًا. حاول التوضيح أكثر. التقييم: 3/10"
    elif any(word in actual_tafsir for word in user_tafsir.strip().split()):
        return "✅ جيد، التفسير يحتوي على كلمات من التفسير الرسمي. التقييم: 7/10"
    else:
        return "❌ التفسير غير واضح أو لا يتطابق مع التفسير الرسمي. التقييم: 4/10"


def app():
    apply_custom_styles()

    st.markdown("<h1 class='title'>📖 رفيق القرآن - مراجعة وحفظ وتفسير</h1>", unsafe_allow_html=True)

    ayah_fetcher = AyahFetcher()
    tafsir_fetcher = TafsirFetcher()
    text_processor = TextProcessor()
    surahs = get_surahs()

    if 'started' not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        surah_name = st.selectbox("اختر السورة", ["اختر السورة..."] + list(surahs.keys()))
        if surah_name == "اختر السورة...":
            st.stop()

        st.session_state.surah_name = surah_name
        st.session_state.surah_id = surahs[surah_name]

        st.session_state.start_ayah = st.number_input("من الآية رقم", min_value=1, value=1, key="start")
        st.session_state.end_ayah = st.number_input("إلى الآية رقم", min_value=st.session_state.start_ayah,
                                                   value=st.session_state.start_ayah, key="end")

        if st.button("✅ ابدأ الإختبار"):
            st.session_state.started = True
            st.rerun()

    else:
        responses = []

        for ayah_num in range(st.session_state.start_ayah, st.session_state.end_ayah + 1):
            st.markdown(f"<hr/><h3>الآية {ayah_num}</h3>", unsafe_allow_html=True)

            actual_ayah = ayah_fetcher.get_ayah_text(st.session_state.surah_id, ayah_num)
            tafsir_text = tafsir_fetcher.get_tafsir(st.session_state.surah_id, ayah_num)

            words = actual_ayah.split()
            prompt_prefix = " ".join(words[:2]) if len(words) > 2 else actual_ayah

            st.markdown(f"### 🧠 اختبار الحفظ\nأكمل بعد: **{prompt_prefix}...**")
            user_input = st.text_area("أكمل الآية:", key=f"mem_{ayah_num}")

            if user_input.strip():
                full_input = prompt_prefix + " " + user_input.strip()
                score = text_processor.compare_ayah(full_input, actual_ayah)
                st.markdown(render_score_visual(score), unsafe_allow_html=True)
            else:
                score = "-"

            st.markdown("### 📘 التفسير")
            user_tafsir = st.text_area("اشرح معنى الآية أو الكلمات:", key=f"tafsir_{ayah_num}")
            tafsir_eval = simple_tafsir_evaluation(user_tafsir, tafsir_text)
            st.info(f"🧾 تقييم التفسير: {tafsir_eval}")

            responses.append([
                st.session_state.surah_name,
                ayah_num,
                user_input,
                f"{score}%" if score != "-" else "-",
                user_tafsir,
                tafsir_eval
            ])

        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["السورة", "رقم الآية", "محاولة الحفظ", "تقييم الحفظ", "محاولة التفسير", "تقييم التفسير"])
        writer.writerows(responses)

        st.download_button(
            label="💾 تحميل النتيجة كملف",
            data=csv_buffer.getvalue().encode('utf-8-sig'),
            file_name="نتائج_مراجعة_القرآن.csv",
            mime="text/csv"
        )

        if st.button("🔁 ابدأ من جديد"):
            st.session_state.started = False
            st.rerun()

if __name__ == "__main__":
    app()
