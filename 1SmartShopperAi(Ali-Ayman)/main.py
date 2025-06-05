# main.py  ─  SmartShopper AI – Rankyx Procurement Assistant
# ---------------------------------------------------------------------------

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import os, traceback
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Rankyx CrewAI imports
# ---------------------------------------------------------------------------
from Agents.keywords_Search_Agent0 import create_keywords_search_agent
from Agents.Search_engine_Agent1   import Search_engine_agent
from Agents.Scraping_Agent2        import Scraping_agent
from Agents.final_reporter_agent3  import Report_maker_Agent

from Tasks.Create_Keywords_search_Task import create_keywords_search_task
from Tasks.Search_engine_task1         import search_engine_task
from Tasks.Scraping_task2              import Scraping_task
from Tasks.final_Reporter_task3        import final_Reporter_task

from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai import Crew, Process, LLM
# ---------------------------------------------------------------------------
load_dotenv()


class SmartShopperStreamlit:
    # ───────────────────────────────────────────────────────────────────
    #  Init & page setup
    # ───────────────────────────────────────────────────────────────────
    def __init__(self):
        st.set_page_config(
            page_title="SmartShopper AI",
            page_icon="🛒",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        self._inject_css()

        st.session_state.setdefault("html_report", None)
        st.session_state.setdefault("raw_results", None)
        st.session_state.setdefault("show_html", False)   # <- toggle for preview

    # ───────────────────────────────────────────────────────────────────
    #  Styling
    # ───────────────────────────────────────────────────────────────────
    def _inject_css(self):
        st.markdown(
            """
            <style>
              @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
              html, body, div, span, input {font-family:'Poppins',sans-serif !important;}
              body {background: radial-gradient(circle at 25% 15%, #e6eeff 0%, #ffffff 55%);}
              .gradient-text{
                background:-webkit-linear-gradient(45deg,#2b7cff,#ff4d9d);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
              .stButton>button{
                background:linear-gradient(90deg,#2b7cff,#ff4d9d);
                border:none;color:#fff;font-weight:600;box-shadow:0 4px 10px rgba(0,0,0,.15);
                transition:.25s;}
              .stButton>button:hover{transform:translateY(-2px) scale(1.03);box-shadow:0 6px 16px rgba(0,0,0,.25);}
              .report-card{background:#ffffffdd;padding:2rem;border-radius:1.2rem;
                box-shadow:0 4px 12px rgba(0,0,0,.08);backdrop-filter:blur(6px);}
            </style>
            """,
            unsafe_allow_html=True,
        )

    # ───────────────────────────────────────────────────────────────────
    #  LLM factory
    # ───────────────────────────────────────────────────────────────────
    @staticmethod
    def _create_llm() -> LLM:
        return LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("DEEP_SEEK_API_KEY"),
            temperature=0.0,
        )

    # ───────────────────────────────────────────────────────────────────
    #  Crew workflow (cached)
    # ───────────────────────────────────────────────────────────────────
    @st.cache_data(show_spinner=False)
    def _run_crew_workflow(
        _self,
        product_name: str,
        websites: list[str],
        country: str,
        language: str,
        keywords_count: int,
    ):
        """Runs CrewAI and returns (html_report_str, raw_output)."""
        self = _self
        llm = self._create_llm()

        ctx = StringKnowledgeSource(
            content="Rankyx provides AI solutions to refine search and recommendation systems."
        )

        kw_agent  = create_keywords_search_agent(llm)
        se_agent  = Search_engine_agent(llm)
        sc_agent  = Scraping_agent(llm)
        rep_agent = Report_maker_Agent(llm)

        kw_task  = create_keywords_search_task(
            product_name, websites, country, keywords_count, language, kw_agent)
        se_task  = search_engine_task(0.5, se_agent)
        sc_task  = Scraping_task(keywords_count, sc_agent)
        rep_task = final_Reporter_task(rep_agent)

        crew = Crew(
            agents=[kw_agent, se_agent, sc_agent, rep_agent],
            tasks=[kw_task, se_task, sc_task, rep_task],
            process=Process.sequential,
            knowledge_sources=[ctx],
        )

        try:
            raw_result = crew.kickoff()
            if hasattr(raw_result, "output"):
                html = raw_result.output
            elif hasattr(raw_result, "final_output"):
                html = raw_result.final_output
            else:
                html = str(raw_result)
            return str(html), raw_result
        except Exception as e:
            st.error("Crew workflow failed:")
            st.error(e)
            st.error(traceback.format_exc())
            return None, None

    # ───────────────────────────────────────────────────────────────────
    #  Sidebar
    # ───────────────────────────────────────────────────────────────────
    def _sidebar_inputs(self):
        st.sidebar.header("🛠️ Configuration")

        product  = st.sidebar.text_input("Product", placeholder="e.g., iPhone 15")
        country  = st.sidebar.selectbox("Target Country",
                                        ["Egypt", "UAE", "Saudi Arabia", "Qatar"])
        websites = st.sidebar.multiselect(
            "Websites", ["amazon.eg","noon.eg","souq.com","jumia.eg","apple.com"],
            default=["amazon.eg","noon.eg"])
        language = st.sidebar.radio("Language", ["english","arabic"], horizontal=True)
        kw_count = st.sidebar.slider("Number of search queries", 5, 20, 10)

        run_btn  = st.sidebar.button("🚀 Generate report", use_container_width=True)
        return run_btn, product, country, websites, language, kw_count

    # ───────────────────────────────────────────────────────────────────
    #  Hero
    # ───────────────────────────────────────────────────────────────────
    def _hero(self):
        st.markdown(
            """
            <h1 class="gradient-text" style="font-size:3rem;font-weight:700;margin:0 0 .2em 0;">
              SmartShopper&nbsp;AI
            </h1>
            <span style="font-size:1.05rem;">
              Your AI-powered product procurement assistant by <b>Rankyx</b>.
            </span>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

    # ───────────────────────────────────────────────────────────────────
    #  Main
    # ───────────────────────────────────────────────────────────────────
    def main(self):
        run_btn, product, country, sites, lang, kw_cnt = self._sidebar_inputs()
        self._hero()

        if run_btn:
            if not product or not sites:
                st.warning("Please enter a product name and choose at least one site.")
            else:
                with st.spinner("Gathering data & preparing your customised report…"):
                    html, raw = self._run_crew_workflow(product, sites, country, lang, kw_cnt)
                    st.session_state.html_report = html
                    st.session_state.raw_results = raw
                    st.session_state.show_html  = False   # reset preview toggle

        # ---------- Results section --------------------------------------
        if st.session_state.html_report:
            st.success("✅ Report generated successfully!", icon="🎉")

            # Buttons row
            col1, col2, col3 = st.columns([1,1,2])
            with col1:
                st.download_button(
                    "💾 Download HTML",
                    data=st.session_state.html_report.encode("utf-8"),
                    file_name=f"SmartShopper_{datetime.now():%Y%m%d_%H%M%S}.html",
                    mime="text/html",
                    use_container_width=True,
                )
            with col2:
                if st.button(
                    ("👁️ Preview HTML" if not st.session_state.show_html
                     else "🙈 Hide Preview"),
                    key="preview_btn",
                    use_container_width=True,
                ):
                    st.session_state.show_html = not st.session_state.show_html

            # Conditional preview
            if st.session_state.show_html:
                st.markdown("<div class='report-card'>", unsafe_allow_html=True)
                st.markdown(st.session_state.html_report, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Raw results expander always available
            with col3:
                with st.expander("📊 Raw results"):
                    st.json(st.session_state.raw_results)

    def run(self):
        self.main()


def main():
    SmartShopperStreamlit().run()


if __name__ == "__main__":
    main()