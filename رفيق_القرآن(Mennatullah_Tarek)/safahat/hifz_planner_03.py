import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
from io import BytesIO

# ===================== THEME & ENVIRONMENT =====================
class PlanEnvironment:
    def __init__(self):
        self.default_theme = {
            "primary": "#2E7D32",
            "secondary": "#00796B",
            "accent": "#FFC107",
            "background": "#F9F9F9",
            "text": "#333333",
            "highlight": "#E6F4EA"
        }

    def get_theme(self):
        return self.default_theme

# ===================== PLAN LOGIC =====================
class HifzPlanner:
    def create_plan(self, from_ayah, to_ayah, total_days):
        total_ayahs = to_ayah - from_ayah + 1
        ayahs_per_day = math.ceil(total_ayahs / total_days)
        plan = []
        current_ayah = from_ayah

        for day in range(1, total_days + 1):
            start = current_ayah
            end = min(current_ayah + ayahs_per_day - 1, to_ayah)

            if day % 7 == 0:
                note = "مراجعة عامة"
            elif day % 5 == 0:
                note = "تثبيت الحفظ"
            elif day % 3 == 0:
                note = "راجع ما سبق"
            elif day == 1:
                note = "ابدأ بنية صادقة"
            else:
                note = "واصل الحفظ"

            plan.append({
                "اليوم": f"اليوم {day}",
                "الآيات": f"{start} - {end}",
                "ملاحظات": note
            })

            current_ayah = end + 1
            if current_ayah > to_ayah:
                break

        return pd.DataFrame(plan)

# ===================== UTILS =====================
def plot_plan_table(df):
    fig, ax = plt.subplots(figsize=(7, len(df) * 0.6 + 1))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='right')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return buf

# ===================== UI =====================
def display_ui(theme):
    

    # Custom CSS
    st.markdown(f"""
        <style>
            body {{
                background-color: {theme['background']};
                color: {theme['text']};
            }}
            .title-section {{
                background-color: {theme['primary']};
                color: white;
                padding: 15px;
                font-size: 28px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 20px;
            }}
            .result-title {{
                font-size: 24px;
                color: {theme['secondary']};
                margin-top: 30px;
                margin-bottom: 10px;
            }}

            
        
        button[kind="primary"] {{
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
    
    
        
        .stDownloadButton>button {{
            background-color: #388E3C;
            color: white;
            font-size: 1rem;
            border-radius: 8px;
            padding: 0.4rem 1rem;
            margin-top: 15px;
            border: 2px solid #2E7D32;
            transition: all 0.3s ease;
            font-weight: bold;
            cursor: pointer;
        }}
        
        .stDownloadButton>button:hover {{
            background-color: #1B5E20;
            border-color: #1B5E20;
            transform: scale(1.03);
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title-section">📖 مُخطط الحفظ الذكي</div>', unsafe_allow_html=True)

    with st.expander("🛠️ اضبط خطة الحفظ"):
        col1, col2 = st.columns(2)
        with col1:
            surah_name = st.text_input("📘 اسم السورة", "البقرة")
            from_ayah = st.number_input("✳️ من الآية", min_value=1, value=1)
        with col2:
            to_ayah = st.number_input("🔚 إلى الآية", min_value=from_ayah, value=7)
            total_days = st.number_input("📅 عدد أيام الحفظ", min_value=1, value=7)

        days_per_week = st.slider("🗓️ كم يوم تحفظ في الأسبوع؟", 1, 7, 5)

    st.markdown(f"""
        <div style='background-color:{theme['highlight']}; padding:10px; border-radius:10px;'>
        📌 <strong>ملخص:</strong><br>
        السورة: <strong>{surah_name}</strong> <br>
        الآيات: <strong>{from_ayah} إلى {to_ayah}</strong> <br>
        عدد الأيام: <strong>{total_days}</strong>، أيام الحفظ في الأسبوع: <strong>{days_per_week}</strong>
        </div>
    """, unsafe_allow_html=True)

    if st.button("✨ أنشئ الخطة الآن"):
        planner = HifzPlanner()
        plan_df = planner.create_plan(from_ayah, to_ayah, total_days)

        st.markdown('<div class="result-title">📋 خطة الحفظ التفصيلية:</div>', unsafe_allow_html=True)
        st.table(plan_df)

        col1, col2 = st.columns(2)
        with col1:
            csv = plan_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("⬇️ تحميل كـ CSV", data=csv, file_name="خطة_الحفظ.csv", mime="text/csv")
        with col2:
            img = plot_plan_table(plan_df)
            st.download_button("🖼️ تحميل كصورة", data=img, file_name="خطة_الحفظ.png", mime="image/png")

# ===================== MAIN =====================
def app():
    env = PlanEnvironment()
    theme = env.get_theme()
    display_ui(theme)

if __name__ == "__main__":
    app()
