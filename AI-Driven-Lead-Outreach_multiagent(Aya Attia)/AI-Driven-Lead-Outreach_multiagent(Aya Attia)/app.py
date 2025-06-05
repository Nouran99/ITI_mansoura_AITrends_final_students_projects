import streamlit as st
import os
import sys
import warnings

warnings.filterwarnings('ignore')
sys.setrecursionlimit(5000)

# Environment Setup
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
os.environ["COHERE_API_KEY"] = st.secrets["COHERE_API_KEY"]
os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

# Imports
import google.generativeai as genai
import cohere

from crewai import Crew, Agent, Task, LLM
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
co = cohere.Client(os.environ["COHERE_API_KEY"])

# Dummy Sentiment Tool (no inheritance from BaseTool)
class SentimentAnalysisTool:
    name = "Sentiment Analysis Tool"
    description = "Ensures tone is positive"
    def _run(self, text: str) -> str:
        return "positive"

# Tools
sentiment_tool = SentimentAnalysisTool()
directory_tool = DirectoryReadTool(directory="./instructions")
file_tool = FileReadTool()
search_tool = SerperDevTool()

# LLMs
gemini_llm = LLM(provider="google_ai_studio", model="gemini/gemini-1.5-flash", api_key=os.environ["GEMINI_API_KEY"])
cohere_llm = LLM(provider="cohere", model="command", api_key=os.environ["COHERE_API_KEY"])

# Agents
sales_agent = Agent(
    role="Sales Representative",
    goal="Identify high-value leads",
    backstory="You find potential leads and analyze trends.",
    llm=gemini_llm
)

lead_sales_agent = Agent(
    role="Lead Sales Representative",
    goal="Write personalized outreach",
    backstory="You create messages that engage leads.",
    llm=cohere_llm
)

analyst = Agent(
    role="Analyst",
    goal="Analyze lead data",
    backstory="You turn raw data into clear insights.",
    llm=gemini_llm
)

# Tasks
def create_tasks(lead_name, industry, milestone):
    return [
        Task(
            description=f"Analyze {lead_name}, a company in the {industry} sector. Find decision-makers and needs.",
            expected_output=f"Profile on {lead_name} with people, background, and strategy.",
            tools=[directory_tool, file_tool, search_tool],
            agent=sales_agent
        ),
        Task(
            description="Summarize business impact of collected AI trends and lead info.",
            expected_output="Analytical report with key insights.",
            agent=analyst
        ),
        Task(
            description=f"Create a message for {lead_name} after their {milestone}. Use sentiment tool.",
            expected_output=f"Concise, positive outreach to {lead_name}.",
            tools=[sentiment_tool, search_tool],
            agent=lead_sales_agent
        )
    ]

# Streamlit UI
st.title("🤖 AI-Driven Lead Intelligence & Outreach System")

with st.form("lead_form"):
    lead_name = st.text_input("🧾 Lead Name", "OpenAI")
    industry = st.text_input("🏭 Industry", "AI Research")
    milestone = st.text_input("🎉 Recent Milestone", "API release")
    submitted = st.form_submit_button("Generate Outreach")

if submitted:
    with st.spinner("Analyzing and crafting message..."):
        crew = Crew(
            agents=[sales_agent, analyst, lead_sales_agent],
            tasks=create_tasks(lead_name, industry, milestone),
            verbose=False,
            memory=False
        )
        result = crew.kickoff(inputs={
            "lead_name": lead_name,
            "industry": industry,
            "milestone": milestone
        })

    st.subheader("📩 Final Outreach Message")
    st.markdown(result)

    # Download
    report_path = f"AI_Lead_Report_{lead_name}.md"
    with open(report_path, "w") as f:
        f.write(result)

    with open(report_path, "rb") as file:
        st.download_button("⬇️ Download Outreach Report", file, file_name=report_path)
