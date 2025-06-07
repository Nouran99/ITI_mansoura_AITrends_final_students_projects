import streamlit as st

class QuranAudioAgent:
    def __init__(self):
  
        self.readers = {
            "عبدالباسط عبدالصمد": ("basit", 8),
            "الحصري": ("hus", 8),
            "محمود علي البنا": ("bna", 8),
            "العفاسي": ("afs", 8),
            "ياسر الدوسري": ("yasser", 11),
            "هزاع البلوشي": ("hazza", 11),
            "فارس عباد": ("frs_a", 8),
        }

    
        self.surahs = {
            "الفاتحة": 1,
            "البقرة": 2,
            "آل عمران": 3,
            "النساء": 4,
            "المائدة": 5,
            "الأنعام": 6,
            "الأعراف": 7,
            "الأنفال": 8,
            "التوبة": 9,
            "يونس": 10,
            "هود": 11,
            "يوسف": 12,
            "الرعد": 13,
            "إبراهيم": 14,
            "الحجر": 15,
            "النحل": 16,
            "الإسراء": 17,
            "الكهف": 18,
            "مريم": 19,
            "طه": 20,
            "الأنبياء": 21,
            "الحج": 22,
            "المؤمنون": 23,
            "النور": 24,
            "الفرقان": 25,
            "الشعراء": 26,
            "النمل": 27,
            "القصص": 28,
            "العنكبوت": 29,
            "الروم": 30,
            "لقمان": 31,
            "السجدة": 32,
            "الأحزاب": 33,
            "سبأ": 34,
            "فاطر": 35,
            "يس": 36,
            "الصافات": 37,
            "ص": 38,
            "الزمر": 39,
            "غافر": 40,
            "فصلت": 41,
            "الشورى": 42,
            "الزخرف": 43,
            "الدخان": 44,
            "الجاثية": 45,
            "الأحقاف": 46,
            "محمد": 47,
            "الفتح": 48,
            "الحجرات": 49,
            "ق": 50,
            "الذاريات": 51,
            "الطور": 52,
            "النجم": 53,
            "القمر": 54,
            "الرحمن": 55,
            "الواقعة": 56,
            "الحديد": 57,
            "المجادلة": 58,
            "الحشر": 59,
            "الممتحنة": 60,
            "الصف": 61,
            "الجمعة": 62,
            "المنافقون": 63,
            "التغابن": 64,
            "الطلاق": 65,
            "التحريم": 66,
            "الملك": 67,
            "القلم": 68,
            "الحاقة": 69,
            "المعارج": 70,
            "نوح": 71,
            "الجن": 72,
            "المزّمّل": 73,
            "المدّثر": 74,
            "القيامة": 75,
            "الإنسان": 76,
            "المرسلات": 77,
            "النبأ": 78,
            "النازعات": 79,
            "عبس": 80,
            "التكوير": 81,
            "الإنفطار": 82,
            "المطفّفين": 83,
            "الإنشقاق": 84,
            "البروج": 85,
            "الطارق": 86,
            "الأعلى": 87,
            "الغاشية": 88,
            "الفجر": 89,
            "البلد": 90,
            "الشمس": 91,
            "الليل": 92,
            "الضحى": 93,
            "الشرح": 94,
            "التين": 95,
            "العلق": 96,
            "القدر": 97,
            "البينة": 98,
            "الزلزلة": 99,
            "العاديات": 100,
            "القارعة": 101,
            "التكاثر": 102,
            "العصر": 103,
            "الهمزة": 104,
            "الفيل": 105,
            "قريش": 106,
            "الماعون": 107,
            "الكوثر": 108,
            "الكافرون": 109,
            "النصر": 110,
            "المسد": 111,
            "الإخلاص": 112,
            "الفلق": 113,
            "الناس": 114
        }

        self.theme = {
            "primary": "#2E7D32",
            "secondary": "#00796B",
            "accent": "#FFC107",
            "background": "#F9F9F9",
            "text": "#333333",
            "highlight": "#AED581"
        }

    def get_audio_url(self, reader_slug, server_num, surah_num):
        if reader_slug == "hus":
            return f"https://server{server_num}.mp3quran.net/husr/{surah_num:03d}.mp3"
        else:
            return f"https://server{server_num}.mp3quran.net/{reader_slug}/{surah_num:03d}.mp3"

    def render_ui(self):
        
        st.markdown(f"""
            <style>
                html, body, .main {{
                    background-color: {self.theme['background']};
                }}
                .title-section {{
                    text-align: center;
                    color: {self.theme['primary']};
                    font-size: 2.5rem;
                    font-weight: 800;
                    margin-bottom: 20px;
                    direction: rtl;
                }}
                .subtitle {{
                    text-align: center;
                    color: {self.theme['secondary']};
                    font-size: 1.2rem;
                    margin-bottom: 40px;
                    direction: rtl;
                }}
                .selects {{
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    max-width: 500px;
                    margin: auto;
                    direction: rtl;
                }}
                .audio-title {{
                    text-align: center;
                    font-size: 1.2rem;
                    color: {self.theme['text']};
                    margin-top: 30px;
                    font-weight: 700;
                }}
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="title-section">الاستماع للقرآن الكريم</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">اختر القارئ والسورة واستمتع بالاستماع بتدبر وخشوع 💖🎧</div>', unsafe_allow_html=True)

        st.markdown('<div class="selects">', unsafe_allow_html=True)
        reader_choice = st.selectbox("🎙️ اختر القارئ:", list(self.readers.keys()))
        surah_choice = st.selectbox("📖 اختر السورة:", list(self.surahs.keys()))
        st.markdown('</div>', unsafe_allow_html=True)

        if reader_choice and surah_choice:
            reader_slug, server_num = self.readers[reader_choice]
            surah_num = self.surahs[surah_choice]
            url = self.get_audio_url(reader_slug, server_num, surah_num)

            st.markdown(f'<div class="audio-title">🎧 القارئ: {reader_choice} | سورة {surah_choice}</div>', unsafe_allow_html=True)
            st.audio(url, format="audio/mp3")

def app():
    agent = QuranAudioAgent()
    agent.render_ui()

if __name__ == "__main__":
    app()
