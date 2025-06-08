import os
import sys
import warnings
import re
from datetime import datetime
import gradio as gr

warnings.filterwarnings('ignore')
sys.setrecursionlimit(5000)

# --- API keys and imports for CrewAI and APIs ---
# Note: You must configure your environment variables or set your API keys here directly
gemini_api_key = os.getenv("GEMINI_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

import google.generativeai as genai
import cohere

from crewai import Crew, Agent, Task, LLM
from crewai_tools import SerperDevTool

# Initialize APIs
genai.configure(api_key=gemini_api_key)
co = cohere.Client(cohere_api_key)

# Initialize LLMs
gemini_llm = LLM(provider="google_ai_studio", model="gemini/gemini-1.5-flash", api_key=gemini_api_key)
cohere_llm = LLM(provider="cohere", model="command", api_key=cohere_api_key)

# Initialize search tool
search_tool = SerperDevTool()

# Define Agents
book_agent = Agent(
    role="Book Finder",
    goal="Find informative and free books related to a given topic.",
    backstory="You help users expand their knowledge by recommending relevant books (PDFs or from platforms like Zlibrary or PDF Drive).",
    llm=gemini_llm,
    tools=[search_tool],
    allow_delegation=False
)

podcast_agent = Agent(
    role="Podcast Curator",
    goal="Find engaging podcasts that match the user's learning goals.",
    backstory="You're great at spotting valuable English podcasts in the user's topic.",
    llm=gemini_llm,
    tools=[search_tool],
    allow_delegation=False
)

youtube_agent = Agent(
    role="YouTube Explorer",
    goal="Find educational YouTube videos and summaries for a topic.",
    backstory="You help users learn visually by recommending the best educational videos available.",
    llm=gemini_llm,
    tools=[search_tool],
    allow_delegation=False
)

# Define Tasks
book_task = Task(
    description="Find 2 books or PDFs for topic: {topic}. Include title and access link if possible.",
    expected_output="List of books with links.",
    agent=book_agent
)

podcast_task = Task(
    description="Find 2 podcast episodes related to topic: {topic}. Include link + short description.",
    expected_output="Podcast links + short context.",
    agent=podcast_agent
)

youtube_task = Task(
    description="Find 2 YouTube videos that explain {topic} in English. Prefer summaries or simple explainers.",
    expected_output="List of videos with links and why they were selected.",
    agent=youtube_agent
)

# Setup Crew
crew = Crew(
    agents=[book_agent, podcast_agent, youtube_agent],
    tasks=[book_task, podcast_task, youtube_task],
    verbose=False,
    memory=False
)

# Helper functions
def parse_crew_results(result):
    outputs = {
        "books_results": "No books found.",
        "podcasts_results": "No podcasts found.",
        "youtube_results": "No YouTube videos found.",
    }
    for task_output in result.tasks_output:
        agent_name = task_output.agent.lower()
        if "book" in agent_name:
            outputs["books_results"] = task_output.raw.strip()
        elif "podcast" in agent_name:
            outputs["podcasts_results"] = task_output.raw.strip()
        elif "youtube" in agent_name:
            outputs["youtube_results"] = task_output.raw.strip()
    return outputs["books_results"], outputs["podcasts_results"], outputs["youtube_results"]

def convert_to_markdown_links(text):
    lines = text.strip().splitlines()
    md_links = []
    for line in lines:
        url_match = re.search(r'(https?://\S+)', line)
        if url_match:
            url = url_match.group(1)
            title = line.replace(url, "").strip(" -•–:")
            md_links.append(f"- [{title if title else url}]({url})")
        else:
            if line.strip():
                md_links.append(f"- {line.strip()}")
    return "\n".join(md_links) if md_links else "No results found."

def convert_to_html_links(text):
    # Simple HTML conversion for Gradio Markdown display
    lines = text.strip().splitlines()
    html_lines = []
    for line in lines:
        url_match = re.search(r'(https?://\S+)', line)
        if url_match:
            url = url_match.group(1)
            title = line.replace(url, "").strip(" -•–:")
            title = title if title else url
            html_lines.append(f'<li><a href="{url}" target="_blank">{title}</a></li>')
        else:
            if line.strip():
                html_lines.append(f'<li>{line.strip()}</li>')
    if html_lines:
        return "<ul>" + "\n".join(html_lines) + "</ul>"
    else:
        return "No results found."

def run_crew_search(topic):
    if not topic or topic.strip() == "":
        return (
            gr.update(value="Please enter a topic.", visible=True),
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
            None,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    inputs = {"topic": topic}
    result = crew.kickoff(inputs=inputs)
    if not hasattr(result, "tasks_output") or not result.tasks_output:
        return (
            gr.update(value="No result returned from Crew.", visible=True),
            gr.update(value="", visible=False),
            gr.update(value="", visible=False),
            None,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

    books_raw, podcasts_raw, youtube_raw = parse_crew_results(result)
    books_html = convert_to_html_links(books_raw)
    podcasts_html = convert_to_html_links(podcasts_raw)
    youtube_html = convert_to_html_links(youtube_raw)

    markdown_report = f"""# 📘 Knowledge Booster Report
**Topic:** {topic}  
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---
## 📚 Books  
{books_raw}
---
## 🎧 Podcasts  
{podcasts_raw}
---
## 📺 YouTube Videos  
{youtube_raw}
"""
    file_path = f"{topic.replace(' ', '_')}_report.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_report)

    show_books = bool(books_raw.strip()) and books_raw.strip().lower() != "no books found."
    show_podcasts = bool(podcasts_raw.strip()) and podcasts_raw.strip().lower() != "no podcasts found."
    show_youtube = bool(youtube_raw.strip()) and youtube_raw.strip().lower() != "no youtube videos found."
    show_download = file_path is not None

    return (
        gr.update(value=books_html, visible=show_books),
        gr.update(value=podcasts_html, visible=show_podcasts),
        gr.update(value=youtube_html, visible=show_youtube),
        file_path,
        gr.update(visible=show_books),     # books_title
        gr.update(visible=show_books),     # sep1
        gr.update(visible=show_podcasts),  # podcasts_title
        gr.update(visible=show_podcasts),  # sep2
        gr.update(visible=show_youtube),   # youtube_title
    )

# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🤗💡 Knowledge Booster with CrewAI")
    gr.Image("woman-7780330_1280.png", elem_id="header-img", show_label=False)
    topic_input = gr.Textbox(label="Enter a Topic", placeholder="e.g., Artificial Intelligence", interactive=True)
    search_btn = gr.Button("🔍 Search")

    # Section titles and separators
    books_title = gr.Markdown("## 📚 Books", visible=False)
    sep1 = gr.Markdown("---", visible=False)
    books_out = gr.Markdown(visible=False)

    podcasts_title = gr.Markdown("## 🎧 Podcasts", visible=False)
    sep2 = gr.Markdown("---", visible=False)
    podcasts_out = gr.Markdown(visible=False)

    youtube_title = gr.Markdown("## 📺 YouTube Videos", visible=False)
    youtube_out = gr.Markdown(visible=False)

    download_btn = gr.File(label="📥 Download Full Report (Markdown)", visible=False)

    search_btn.click(
        fn=run_crew_search,
        inputs=topic_input,
        outputs=[
            books_out,
            podcasts_out,
            youtube_out,
            download_btn,
            books_title,
            sep1,
            podcasts_title,
            sep2,
            youtube_title
        ]
    )

demo.launch()
