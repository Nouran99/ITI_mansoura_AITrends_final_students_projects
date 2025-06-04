from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from pydantic import BaseModel, Field
from typing import List
from tavily import TavilyClient
from scrapegraph_py import Client
from serpapi import GoogleSearch
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from Agents import load_llm
from Agents import AgentA
from Agents import AgentB
from Agents import AgentC
from Agents import AgentD
import streamlit as st




no_keywords = 1

about_company = "Rankyx is a company that provides AI solutions to help websites refine their search and recommendation systems."

company_context = StringKnowledgeSource(
    content=about_company
)
llm=load_llm
search_queries_recommendation_agent,search_queries_recommendation_task=AgentA()
search_engine_agent,search_engine_task=AgentB()
scrape_agent,scrape_task=AgentC()
summarization_agent,summarization_task=AgentD()

crew = Crew(
    agents=[
        search_queries_recommendation_agent,
        search_engine_agent,
        scrape_agent,
        summarization_agent,
    ],
    tasks=[
        search_queries_recommendation_task,
        search_engine_task,
        scrape_task,
        summarization_task,
    ],
    process=Process.sequential,
    knowledge_sources=[company_context]
)

SCRAPED_PATH = "ai-agent-output/scraped_papers.json"
SUMMARY_PATH = "ai-agent-output/final_summaries.json"

def kickoff_pipeline(topic: str):
    crew_results = crew.kickoff(
        inputs={
            "research_topic": topic,
            "no_keywords": 2,
            "score_th": 0.5,
            "top_recommendations_no": 10
        }
    )
    return crew_results

def load_summaries():
    if os.path.exists(SUMMARY_PATH):
        with open(SUMMARY_PATH, "r") as f:
            data = json.load(f)
            return data.get("summaries", [])
    return []

# Streamlit UI
st.set_page_config(page_title="Research Summarizer", layout="wide")
st.title("🧠 Academic Research Paper Summarizer")
st.write("Enter a research keyword to discover and summarize recent academic papers.")

topic = st.text_input("🔍 Enter research keyword:")

if st.button("Run Research Agent"):
    with st.spinner("⏳ Running CrewAI agents and summarizing papers..."):
        kickoff_pipeline(topic)
        summaries = load_summaries()

    if summaries:
        st.success(f"✅ Found {len(summaries)} paper summaries.")
        for paper in summaries:
            st.markdown("---")
            st.markdown(f"### 🔖 {paper['title']}")
            st.markdown(f"[🔗 View Paper]({paper['url']})")
            st.markdown(f"📄 **Summary:**\n\n{paper['summary']}")
    else:
        st.warning("No summaries were generated or the papers had no valid sections.")

