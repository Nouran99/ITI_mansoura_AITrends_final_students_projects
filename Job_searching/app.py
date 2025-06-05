__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import os
from pydantic import BaseModel, Field
from typing import List
from crewai import Crew, Agent, Task, Process, LLM
from crewai.tools import tool
from tavily import TavilyClient
from scrapegraph_py import Client
import zipfile
from io import BytesIO
import json

# output folder path 
output_dir = "./ai-agent-output"
os.makedirs(output_dir, exist_ok=True)

# environment
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# general setup for the llm model
basic_llm = LLM(
    model="gemini/gemini-1.5-flash",
    temperature=0,
    provider="google_ai_studio",
    api_key=os.environ["GEMINI_API_KEY"]
)

# Agent 1
the_max_queries = 20

class search_recommendation(BaseModel):
    search_queries: List[str] = Field(..., title="Recommended searches to be sent to the search engines", min_items=1, max_items=the_max_queries)

search_recommendation_agent = Agent(
    role="search_recommendation_agent",
    goal="""to provide a list of recommendations search queries to be passed to the search engine.
    The queries must be varied and looking for specific items""",
    backstory="The agent is designed to help in looking for products by providing a list of suggested search queries to be passed to the search engine based on the context provided.",
    llm=basic_llm,
    verbose=True,
)

search_recommendation_task = Task(
    description="\n".join([
        "Mariam is looking for a job as {job_name}",
        "so the job must be suitable for {level}",
        "The search query must take the best offers",
        "I need links of the jobs",
        "The recommended query must not be more than {the_max_queries}",
        "The job must be in {country_name}"
    ]),
    expected_output="A JSON object containing a list of suggested search queries.",
    output_json=search_recommendation,
    agent=search_recommendation_agent,
    output_file=os.path.join(output_dir, "step_1_Recommend_search_queries.json"),
)

# Agent 2
search_clint = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

class SingleSearchResult(BaseModel):
    title: str
    url: str = Field(..., title="the page url")
    content: str
    score: float
    search_query: str

class AllSearchResults(BaseModel):
    results: List[SingleSearchResult]

@tool
def search_engine_tool(query: str):
    """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
    return search_clint.search(query)

search_engine_agent = Agent(
    role="search engine agent",
    goal="To search on job based on suggested search queries",
    backstory="that agent designed to help in finding jobs by using the suggested search queries",
    llm=basic_llm,
    verbose=True,
    tools=[search_engine_tool]
)

search_engine_task = Task(
    description="\n".join([
        "search for jobs based on the suggested search queries",
        "you have to collect results from the suggested search queries",
        "ignore any results that are not related to the job",
        "Ignore any search results with confidence score less than ({score_th})",
        "the search result will be used to summarize the posts to understand what the candidate needs to have",
        "you should give me more than 10 jobs"
    ]),
    expected_output="A JSON object containing search results.",
    output_json=AllSearchResults,
    agent=search_engine_agent,
    output_file=os.path.join(output_dir, "step_2_search_results.json")
)

# Agent 3
scrape_client = Client(api_key=st.secrets["SCRAPEGRAPH_API_KEY"])

class ProductSpec(BaseModel):
    specification_name: str
    specification_value: str

class SingleExtractedProduct(BaseModel):
    page_url: str = Field(..., title="The original url of the job page")
    Job_Requirements: str = Field(..., title="The requirements of the job")
    Job_Title: str = Field(..., title="The title of the job")
    Job_Details: str = Field(title="The Details of the job", default=None)
    Job_Description: str = Field(..., title="The Description of the job")
    Job_Location: str = Field(title="The location of the job", default=None)
    Job_Salary: str = Field(title="The salary of the job", default=None)
    Job_responsability: str = Field(..., title="The responsibility of the job")
    Job_type: str = Field(title="The type of the job", default=None)
    Job_Overview: str = Field(..., title="The overview of the job")
    qualifications: str = Field(..., title="The qualifications of the job")
    product_specs: List[ProductSpec] = Field(..., title="The specifications of the product. Focus on the most important requirements.", min_items=1, max_items=5)
    agent_recommendation_notes: List[str] = Field(..., title="A set of notes why would you recommend or not recommend this job to the candidate, compared to other jobs.")

class AllExtractedProducts(BaseModel):
    products: List[SingleExtractedProduct]

@tool
def web_scraping_tool(page_url: str):
    """An AI Tool to help an agent to scrape a web page"""
    details = scrape_client.smartscraper(
        website_url=page_url,
        user_prompt="Extract ```json\n" + SingleExtractedProduct.schema_json() + "```\n From the web page"
    )
    return {
        "page_url": page_url,
        "details": details
    }

search_scrap_agent = Agent(
    role="Web scrap agent to extract url information",
    goal="to extract information from any website",
    backstory="the agent designed to extract required information from any website and that information will be used to understand which skills the jobs need",
    llm=basic_llm,
    verbose=True,
    tools=[web_scraping_tool]
)

search_scrap_task = Task(
    description="\n".join([
        "The task is to extract job details from any job offer page url.",
        "The task has to collect results from multiple pages urls.",
        "you should focus on what requirements or qualification or responsibilities",
        "the results from you the user will use it to understand which skills he needs to have",
        "I need you to give me more than +5 jobs"
    ]),
    expected_output="A JSON object containing jobs details",
    output_json=AllExtractedProducts,
    output_file=os.path.join(output_dir, "step_3_search_results.json"),
    agent=search_scrap_agent
)

# Agent 4
search_summarize_agent = Agent(
    role="extract information about what requirements for every job",
    goal="to extract information about what requirements for every job",
    backstory="the agent should detect what requirements for the job according to the job description and requirements",
    llm=basic_llm,
    verbose=True,
)

search_summarize_task = Task(
    description="\n".join([
        "extract what skills should the candidate of that job should have",
        "you have to collect results about what each job skills need",
        "ignore any results that have None values",
        "Ignore any search results with confidence score less than ({score_th})",
        "the candidate needs to understand what skills he should have",
        "you can also recommend skills from understanding jobs title even if it is not in the job description",
        "I need you to give me +10 skills"
    ]),
    expected_output="Summarize of what skills that job need candidate to have",
    agent=search_summarize_agent,
    output_file=os.path.join(output_dir, "step_4_search_results.json")
)

Company_Crew = Crew(
    process=Process.sequential,
    agents=[search_recommendation_agent, search_engine_agent, search_scrap_agent, search_summarize_agent],
    tasks=[search_recommendation_task, search_engine_task, search_scrap_task, search_summarize_task]
)
######################## Streamlit UI #######################

st.title("Job Search AI Crew")

choice_job = st.text_input("Enter the job title (e.g., AI developer):")
choice_level = st.text_input("Enter the level (e.g., Junior):")
choice_region = st.text_input("Enter the region (e.g., Egypt):")

if "crew_ran" not in st.session_state:
    st.session_state.crew_ran = False

if st.button("Run Crew"):
    if choice_job and choice_level and choice_region:
        with st.spinner("Crew is running, please wait... ⏳"):
            crew_results = Company_Crew.kickoff(
                inputs={
                    "job_name": f"job offer for {choice_job}",
                    "the_max_queries": 20,
                    "level": choice_level,
                    "score_th": 0.02,
                    "country_name": choice_region
                }
            )
        st.success("Crew finished running!")
        st.session_state.crew_ran = True
    else:
        st.warning("Please enter job title, level, and region.")

if st.session_state.crew_ran:
   # Define your file names and their friendly labels
    files_and_labels = [
        ("step_1_Recommend_search_queries.json", "🔍 Recommended Search Queries"),
        ("step_2_search_results.json", "🌐 Search Results"),
        ("step_3_search_results.json", "🧾 Extracted Job Details"),
        ("step_4_search_results.json", "🧠 Summarized Skills")
    ]

    # Title for the Streamlit app
    st.title("💼 Job Search AI Crew - Results Viewer")

    # Loop through each file and display its contents in a user-friendly way
    for filename, label in files_and_labels:
        file_path = os.path.join(output_dir, filename)
        if os.path.exists(file_path):
            st.subheader(label)
            try:
                # Special handling for the last summary file (step_4_search_results.json)
                if filename == "step_4_search_results.json":
                    with open(file_path, "r", encoding="utf-8") as f:
                        summary_text = f.read()
                    # Just display as markdown/plain text
                    st.markdown(summary_text)
                else:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Display based on the type of data
                    if isinstance(data, dict):
                        if "search_queries" in data:
                            st.markdown("### Suggested Search Queries")
                            for i, query in enumerate(data["search_queries"], 1):
                                st.markdown(f"**{i}.** {query}")
                        elif "results" in data:
                            st.markdown("### Search Engine Results")
                            for result in data["results"]:
                                with st.expander(result.get("title", "Job Result")):
                                    st.markdown(f"**🔗 URL**: [{result['url']}]({result['url']})")
                                    st.markdown(f"**📊 Score**: {result['score']}")
                                    st.markdown(f"**🔍 Query**: {result['search_query']}")
                                    st.markdown(f"**📄 Content**: {result['content']}")
                        elif "products" in data:
                            st.markdown("### Extracted Job Details")
                            for product in data["products"]:
                                with st.expander(product.get("Job_Title", "Job Listing")):
                                    st.markdown(f"**🔗 URL**: [{product['page_url']}]({product['page_url']})")
                                    st.markdown(f"**📌 Overview**: {product['Job_Overview']}")
                                    st.markdown(f"**🧠 Requirements**: {product['Job_Requirements']}")
                                    st.markdown(f"**📝 Responsibilities**: {product['Job_responsability']}")
                                    st.markdown(f"**🎓 Qualifications**: {product['qualifications']}")
                                    if product.get("product_specs"):
                                        st.markdown("**🔧 Top Specifications:**")
                                        for spec in product['product_specs']:
                                            st.markdown(f"- **{spec['specification_name']}**: {spec['specification_value']}")
                        else:
                            st.json(data)
                    else:
                        st.json(data)
            except json.JSONDecodeError:
                st.error(f"{filename} could not be decoded as valid JSON.")
        else:
            st.warning(f"File {filename} not found.")
