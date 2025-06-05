from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from pydantic import BaseModel, Field
from typing import List
from tavily import TavilyClient
import os
import json
import threading
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    OUTPUT_DIR = "./ai-agent-output"
    RESULTS_NUM = 5

# Initialize LLM and Search Client
os.environ["GEMINI_API_KEY"] = Config.GEMINI_API_KEY
basic_llm = LLM(model="gemini/gemini-1.5-flash", temperature=0)
search_client = TavilyClient(api_key=Config.TAVILY_API_KEY)

# Create output directory
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

# Pydantic Models
class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(..., title="Suggested search queries to help the user self-learn a topic",
                               min_items=1, max_items=10)

class SingleSearchResult(BaseModel):
    title: str
    url: str = Field(..., title="The page URL")

class AllSearchResults(BaseModel):
    results: List[SingleSearchResult]

# Tools
@tool
def visual_search_tool(query: str) -> List[SingleSearchResult]:
    """Searches only within YouTube, Udemy, Coursera for visual resources"""
    try:
        youtube_query = search_client.search(query=query+"site:youtube.com", max_results=Config.RESULTS_NUM)
        udemy_query = search_client.search(query="free"+query+"site:udemy.com", max_results=Config.RESULTS_NUM)
        coursera_query = search_client.search(query="free"+query+"site:coursera.org", max_results=Config.RESULTS_NUM)
        return [youtube_query, udemy_query, coursera_query]
    except Exception as e:
        print(f"Visual search error: {e}")
        return []

@tool
def text_search_tool(query: str) -> List[SingleSearchResult]:
    """Searches only within medium.com, arxiv.org, github.com, paperswithcode.com for text resources"""
    try:
        medium_query = search_client.search(query=query+"site:medium.com", max_results=Config.RESULTS_NUM)
        arxiv_query = search_client.search(query=query+"site:arxiv.org", max_results=Config.RESULTS_NUM)
        github_query = search_client.search(query=query+"site:github.com", max_results=Config.RESULTS_NUM)
        paperswithcode_query = search_client.search(query=query+"site:paperswithcode.com", max_results=Config.RESULTS_NUM)
        return [medium_query, arxiv_query, github_query, paperswithcode_query]
    except Exception as e:
        print(f"Text search error: {e}")
        return []

# Agents
search_queries_recommendation_agent = Agent(
    role="Search Queries Recommendation Agent",
    goal="\n".join([
        "Generate a list of well-structured and general-purpose search queries based on a given learning topic and user level.",
        "Queries should be informative, specific, and useful for self-learning.",
        "Do not include the name of any platform, website, or content type.",
        "The goal is to create queries that can be used in general-purpose search engines."
    ]),
    backstory=(
        "This agent helps learners by generating highly relevant search queries for any topic and skill level. "
        "It avoids mentioning specific sources, allowing downstream agents to handle targeted search in different content formats."
    ),
    llm=basic_llm,
    verbose=True
)

visual_search_agent = Agent(
    role="Visual Learning Resources Agent",
    goal="To find visual educational resources (videos, playlists, courses) based on given search queries.",
    backstory="You specialize in finding helpful video-based learning materials for advanced learners from YouTube, Coursera, Udemy, and Khan Academy.",
    llm=basic_llm,
    verbose=True,
    tools=[visual_search_tool]
)

text_search_agent = Agent(
    role="Textual Learning Resources Agent",
    goal="To find rich, insightful, and trustworthy educational resources from top-tier domains.",
    backstory="You're a research assistant who specializes in discovering valuable content like articles, GitHub repos, research papers, and technical blogs from well-known educational platforms.",
    llm=basic_llm,
    verbose=True,
    tools=[text_search_tool]
)

summary_markdown_agent = Agent(
    role="Markdown Learning Report Designer",
    goal="Create a clean, structured Markdown (.md) report from visual and textual sources.",
    backstory=(
        "This agent builds a clean Markdown summary from visual and textual learning sources. "
        "The format is simple, readable, and structured with bullet points for easy navigation."
    ),
    llm=basic_llm,
    verbose=True,
)

# Store active jobs
active_jobs = {}

def run_learning_crew(job_id, topic_name, learning_level):
    """Run the CrewAI workflow in background"""
    try:
        active_jobs[job_id]['status'] = 'running'
        active_jobs[job_id]['progress'] = 'Initializing agents...'
        
        # Create unique output directory for this job
        job_output_dir = os.path.join(Config.OUTPUT_DIR, f"job_{job_id}")
        os.makedirs(job_output_dir, exist_ok=True)
        
        # Tasks
        search_queries_task = Task(
            description=f"Generate search queries for topic: {topic_name} at {learning_level} level",
            expected_output="A JSON object containing a list of suggested general-purpose search queries.",
            output_json=SuggestedSearchQueries,
            output_file=os.path.join(job_output_dir, "step_1_suggested_search_queries.json"),
            agent=search_queries_recommendation_agent
        )
        
        visual_search_task = Task(
            description=f"Find visual resources for {topic_name} at {learning_level} level",
            expected_output="A JSON file containing valid visual search results.",
            output_json=AllSearchResults,
            output_file=os.path.join(job_output_dir, "step_2_visual_results.json"),
            agent=visual_search_agent
        )
        
        text_search_task = Task(
            description=f"Find textual resources for {topic_name} at {learning_level} level",
            expected_output="A JSON file with the best educational search results.",
            output_json=AllSearchResults,
            output_file=os.path.join(job_output_dir, "step_3_textual_results.json"),
            agent=text_search_agent
        )
        
        summary_task = Task(
            description="Create a structured Markdown report with all resources",
            expected_output="A structured Markdown file with all links.",
            output_file=os.path.join(job_output_dir, "summary_report.md"),
            agent=summary_markdown_agent
        )
        
        # Create and run crew
        active_jobs[job_id]['progress'] = 'Running search agents...'
        
        crew = Crew(
            agents=[search_queries_recommendation_agent, visual_search_agent, text_search_agent, summary_markdown_agent],
            tasks=[search_queries_task, visual_search_task, text_search_task, summary_task],
            process=Process.sequential
        )
        
        result = crew.kickoff(inputs={'topic_name': topic_name, 'learning_level': learning_level})
        
        active_jobs[job_id]['status'] = 'completed'
        active_jobs[job_id]['progress'] = 'Complete!'
        active_jobs[job_id]['result_path'] = job_output_dir
        active_jobs[job_id]['completed_at'] = datetime.now().isoformat()
        
    except Exception as e:
        active_jobs[job_id]['status'] = 'failed'
        active_jobs[job_id]['error'] = str(e)
        print(f"Job {job_id} failed: {e}")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start-learning', methods=['POST'])
def start_learning():
    data = request.json
    topic_name = data.get('topic_name', '').strip()
    learning_level = data.get('learning_level', 'intermediate')
    
    if not topic_name:
        return jsonify({'error': 'Topic name is required'}), 400
    
    # Generate unique job ID
    job_id = f"Resources"
    
    # Initialize job status
    active_jobs[job_id] = {
        'status': 'starting',
        'progress': 'Preparing...',
        'topic': topic_name,
        'level': learning_level,
        'started_at': datetime.now().isoformat()
    }
    
    # Start background task
    thread = threading.Thread(target=run_learning_crew, args=(job_id, topic_name, learning_level))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'started'})

@app.route('/api/job-status/<job_id>')
def job_status(job_id):
    if job_id not in active_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = active_jobs[job_id].copy()
    
    # If completed, try to load results
    if job['status'] == 'completed' and 'result_path' in job:
        try:
            result_path = job['result_path']
            
            # Load summary if exists
            summary_path = os.path.join(result_path, 'summary_report.md')
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    job['summary'] = f.read()
            
            # Load search queries if exists
            queries_path = os.path.join(result_path, 'step_1_suggested_search_queries.json')
            if os.path.exists(queries_path):
                with open(queries_path, 'r', encoding='utf-8') as f:
                    job['queries'] = json.load(f)
                    
        except Exception as e:
            print(f"Error loading results: {e}")
    
    return jsonify(job)

@app.route('/api/download-report/<job_id>')
def download_report(job_id):
    if job_id not in active_jobs or active_jobs[job_id]['status'] != 'completed':
        return jsonify({'error': 'Job not found or not completed'}), 404
    
    result_path = active_jobs[job_id]['result_path']
    summary_path = os.path.join(result_path, 'summary_report.md')
    
    if os.path.exists(summary_path):
        return send_file(summary_path, as_attachment=True, download_name=f"learning_report_{job_id}.md")
    else:
        return jsonify({'error': 'Report file not found'}), 404

if __name__ == '__main__':
    ## for development
    # app.run(debug=True, threaded=True)

    # for production
    app.run(host="0.0.0.0", port=5000)
