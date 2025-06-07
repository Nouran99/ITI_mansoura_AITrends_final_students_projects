import streamlit as st
import random


st.set_page_config(
    page_title="رفيق القرآن",
    layout="wide",
    page_icon="https://cdn-icons-png.flaticon.com/512/4358/4358773.png"
)


theme = {
    "primary": "#2E7D32",
    "secondary": "#009688",
    "accent": "#FFC107",
    "background": "#fffbf2"
}


daily_ayahs = [
    "إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴿٦﴾ - الشرح",
    "وَقُل رَّبِّ زِدْنِي عِلْمًا ﴿١١٤﴾ - طه",
    "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴿١٥٣﴾ - البقرة",
    "فَاذْكُرُونِي أَذْكُرْكُمْ ﴿١٥٢﴾ - البقرة"
]


pages = {
    "🏠 الرئيسية": None,
    "🎧 الاستماع":       "safahat.estimaa_02",
    "🗓️ مُخطط الحفظ":    "safahat.hifz_planner_03",
    "🔁 مُساعد الحفظ":    "safahat.hifz_helper_04",
    "📖 تفسير":         "safahat.tafsir_05",
    "🧠 لعبة المراجعة":  "safahat.moraj3a",
    "❓ سؤال قرآنى":     "safahat.ask_quran",
    "من نحن 👀": "safahat.about_app"
}


query_params = st.query_params
current_page = query_params.get("page", "🏠 الرئيسية")

if current_page not in pages:
    current_page = "🏠 الرئيسية"

def load_page(page_key):
    mod_name = pages.get(page_key)
    if mod_name:
        mod = __import__(mod_name, fromlist=['app'])
        mod.app()


st.markdown(f"""
<style>
    body, .stApp {{
             background-color: {theme['background']};
            direction: rtl;
            font-family: 'Cairo', sans-serif;
        }}

    .fade-in {{
        animation: fadeIn 0.8s ease-in-out;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .main-title {{
        color: {theme['primary']};
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0 10px;
    }}
    .quote {{
        font-size: 18px;
        color: {theme['secondary']};
        text-align: center;
        font-style: italic;
        margin-bottom: 30px;
    }}
    .centered-image img {{
        width: 500px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
        margin: 80px auto 40px auto;
        display: block;
    }}
    .centered-image img:hover {{
        transform: scale(1.05);
    }}
    .bottom-nav {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: {theme['primary']};
        display: flex;
        justify-content: center;
        padding: 12px 0;
        border-top: 3px solid {theme['accent']};
        z-index: 999;
    }}
    .bottom-nav a {{
        color: white;
        margin: 0 15px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        padding: 6px 12px;
        border-radius: 8px;
        transition: background-color 0.3s;
        cursor: pointer;
    }}
    .bottom-nav a:hover {{
        background-color: {theme['accent']};
        color: black;
    }}
    .bottom-nav a.active {{
        background-color: {theme['accent']};
        color: black;
    }}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style="background-color:#2E7D32; padding: 15px; color:white; text-align:center; font-weight:bold; font-size:26px; position: fixed; top:0; width:100%; z-index: 1000;">
    📖 رفيق القرآن
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="fade-in">', unsafe_allow_html=True)

if current_page == "🏠 الرئيسية":
    st.markdown('<div class="main-title" style="margin-top:70px;">  رفيق القرآن : ابدأ رحلتك الآن ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="quote">“خيركم من تعلم القرآن وعلمه” – النبي محمد ﷺ</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="centered-image">
        <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="quote">🌟 مقتطف اليوم: {random.choice(daily_ayahs)}</div>', unsafe_allow_html=True)
else:
    load_page(current_page)

st.markdown('</div>', unsafe_allow_html=True)


footer_html = ""
for page_name in pages.keys():
    active = "active" if page_name == current_page else ""
    footer_html += f'<a href="/?page={page_name}" class="{active}">{page_name}</a>'

st.markdown(f'<div class="bottom-nav">{footer_html}</div>', unsafe_allow_html=True)

