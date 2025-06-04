from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from pydantic import BaseModel, Field
from typing import List
from serpapi import GoogleSearch
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()

def load_llm():
    llm = LLM(
        model="gemini/gemini-1.5-flash",
        verbose=True,
        temperature=0.5,
        api_key=os.getenv("GEMINI_API_KEY")
    )
    return llm

llm=load_llm()
output_dir = "./ai-agent-output"
os.makedirs(output_dir, exist_ok=True)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def AgentA():
    no_keywords = 1

    class SuggestedSearchKeywords(BaseModel):
        keywords: List[str] = Field(
            ...,
            title="Suggested search keywords for scientific research papers",
            min_items=1,
            max_items=no_keywords
        )

    search_queries_recommendation_agent = Agent(
        role="Scientific Search Keywords Recommendation Agent",
        goal="\n".join([
            "To provide a list of concise, precise search keywords for finding scientific research papers.",
            "The keywords should be relevant to the provided research topic and avoid general or ambiguous terms.",
            "The keywords should be suitable for academic search engines like Google Scholar."
        ]),
        backstory="The agent helps generate effective academic search keywords for retrieving scientific papers from search engines like Google Scholar.",
        llm=llm,
        verbose=True,
    )

    search_queries_recommendation_task = Task(
        description="\n".join([
            "Given a research topic or context: {research_topic}",
            "Generate up to {no_keywords} concise and precise keywords or short phrases.",
            "The keywords should be specific and focused on scientific research papers.",
            "Avoid general words and commercial product terms.",
            "The keywords will be used to search scholarly articles via Google Scholar or other academic search engines."
        ]),
        expected_output="A JSON object containing a list of suggested search keywords.",
        output_json=SuggestedSearchKeywords,
        output_file=os.path.join(output_dir, "step_1_suggested_search_keywords.json"),
        agent=search_queries_recommendation_agent
    )
    return search_queries_recommendation_agent,search_queries_recommendation_task

def AgentB():
    class SingleSearchResult(BaseModel):
        title: str
        url: str = Field(..., title="The page URL")
        content: str
        score: float
        search_query: str

    class AllSearchResults(BaseModel):
        results: List[SingleSearchResult]

    @tool
    def search_academic_papers_tool(query: str) -> AllSearchResults:
        """
        Searches Google Scholar for academic papers related to a concept using SerpAPI.
        """
        print(f"[INFO] Searching for: {query}")
        contextual_query = f"{query} in research"
        params = {
            "engine": "google_scholar",
            "q": contextual_query,
            "api_key": SERPAPI_API_KEY
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            print("[DEBUG] Raw SerpAPI response:")
            print(json.dumps(results, indent=2))  # Optional: remove or comment out in prod

            organic_results = results.get("organic_results", [])
            if not organic_results:
                print("[WARN] No organic results found.")
                return AllSearchResults(results=[])
        except Exception as e:
            print(f"[ERROR] SerpAPI request failed: {e}")
            return AllSearchResults(results=[])

        search_results = []
        for result in organic_results:
            title = result.get("title", "No Title")
            url = result.get("link", "")
            content = result.get("snippet", "No Description")
            score = 1.0  # Dummy score for now

            print(f"[DEBUG] Found result: {title} - {url}")

            search_results.append(SingleSearchResult(
                title=title,
                url=url,
                content=content,
                score=score,
                search_query=query
            ))

        return AllSearchResults(results=search_results)

    search_engine_agent = Agent(
        role="Research Paper Search Agent",
        goal="Search for relevant academic papers explaining concepts and applications using trusted academic sources.",
        backstory="This agent assists researchers by searching Google Scholar for papers using SerpAPI.",
        llm=llm,  # Replace with your LLM instance if needed
        verbose=True,
        tools=[search_academic_papers_tool]
    )

    search_engine_task = Task(
        description=(
            "Search academic papers related to the query using Google Scholar via SerpAPI. "
            "Return results including paper title, url, snippet, and a confidence score."
        ),
        expected_output="A JSON object containing the search results as a list of papers.",
        output_json=AllSearchResults,
        output_file=os.path.join(output_dir, "step_2_search_results.json"),
        agent=search_engine_agent
    )

    return search_engine_agent,search_engine_task
def AgentC():
    class ScrapedPaper(BaseModel):
        url: str
        abstract: str = ""
        introduction: str = ""
        methodology: str = ""
        results: str = ""
        dataset: str = ""

    class ScrapedPapers(BaseModel):
        papers: List[ScrapedPaper]

    def scrape_paper_sections(url: str) -> dict:
        """Scrape typical paper sections from a given URL."""
        sections = {
            "abstract": "",
            "introduction": "",
            "methodology": "",
            "results": "",
            "dataset": ""
        }

        try:
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                print(f"[WARN] Failed to fetch {url} with status {res.status_code}")
                return sections
            soup = BeautifulSoup(res.text, "html.parser")

            # Try abstract via ID or class
            abstract = soup.find("section", {"class": "abstract"}) or soup.find("div", {"id": "abstract"})
            if abstract:
                sections["abstract"] = abstract.get_text(separator=" ", strip=True)

            headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])
            for header in headers:
                text = header.get_text(strip=True).lower()
                content = []
                if "introduction" in text or "background" in text:
                    siblings = header.find_next_siblings()
                    for sib in siblings:
                        if sib.name and sib.name.startswith('h'):
                            break
                        content.append(sib.get_text(separator=" ", strip=True))
                    sections["introduction"] = " ".join(content).strip()
                elif "method" in text:
                    siblings = header.find_next_siblings()
                    for sib in siblings:
                        if sib.name and sib.name.startswith('h'):
                            break
                        content.append(sib.get_text(separator=" ", strip=True))
                    sections["methodology"] = " ".join(content).strip()
                elif "result" in text:
                    siblings = header.find_next_siblings()
                    for sib in siblings:
                        if sib.name and sib.name.startswith('h'):
                            break
                        content.append(sib.get_text(separator=" ", strip=True))
                    sections["results"] = " ".join(content).strip()
                elif "data" in text or "dataset" in text:
                    siblings = header.find_next_siblings()
                    for sib in siblings:
                        if sib.name and sib.name.startswith('h'):
                            break
                        content.append(sib.get_text(separator=" ", strip=True))
                    sections["dataset"] = " ".join(content).strip()

        except Exception as e:
            print(f"[ERROR] Error scraping {url}: {e}")

        return sections

    @tool
    def scrape_multiple_papers_tool(search_results_file: str) -> ScrapedPapers:
        """
        Given a JSON file path containing paper search results, scrape each paper's key sections.
        Saves scraped data into output JSON file.
        """
        if not os.path.exists(search_results_file):
            raise FileNotFoundError(f"File not found: {search_results_file}")

        with open(search_results_file, "r") as f:
            data = json.load(f)

        papers = []
        for result in data.get("results", []):
            url = result.get("url")
            if not url:
                continue
            print(f"[INFO] Scraping paper at URL: {url}")
            sections = scrape_paper_sections(url)
            papers.append(ScrapedPaper(url=url, **sections))

        # Save scraped data to output file
        output_path = os.path.join(output_dir, "scraped_papers.json")
        with open(output_path, "w") as out_file:
            json.dump({"papers": [paper.dict() for paper in papers]}, out_file, indent=2)

        print(f"[SUCCESS] Scraped data saved to {output_path}")
        return ScrapedPapers(papers=papers)

    # --- Agent Definition ---
    scrape_agent = Agent(
        role="Paper Scraping Agent",
        goal="Extract academic paper sections like abstract, introduction, methodology, results, and dataset from a given URL.",
        backstory="This agent scrapes structured sections from research paper web pages.",
        verbose=True,
        llm=llm,
        tools=[scrape_multiple_papers_tool]
    )
    scrape_task = Task(
        description="Use the output file from the search engine agent located at 'ai-agent-output/step_2_search_results.json'. "
                    "Scrape each paper URL for abstract, introduction, methodology, results, and dataset sections.",
        expected_output="A JSON file saved as 'ai-agent-output/scraped_papers.json' containing a list of scraped paper sections.",
        input={"search_results_file": os.path.join(output_dir, "step_2_search_results.json")},
        output_file=os.path.join(output_dir, "scraped_papers.json"),
        agent=scrape_agent
    )
    return scrape_agent,scrape_task
def AgentD():
    
    class PaperSummary(BaseModel):
        title: str
        url: str
        summary: str

    class PaperSummaries(BaseModel):
        summaries: List[PaperSummary]

    # --- Tool Function ---
    def summarize_papers_from_scraped_file(file_path: str, llm) -> PaperSummaries:
        """Generates fluent summaries using LLM from a JSON file of scraped paper sections."""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing input JSON file: {file_path}")

        with open(file_path, "r") as f:
            data = json.load(f)

        summaries = []

        for paper in data.get("papers", []):
            url = paper.get("url", "")
            title = paper.get("title", "Untitled")

            # Build a pseudo-summary to feed into LLM
            points = []
            if paper.get("abstract"):
                points.append(f"Abstract: {paper['abstract']}")
            if paper.get("introduction"):
                points.append(f"Introduction: {paper['introduction']}")
            if paper.get("results"):
                points.append(f"Results: {paper['results']}")
            if paper.get("dataset"):
                points.append(f"Dataset: {paper['dataset']}")

            if not points:
                continue  # Skip paper with no useful content

            combined_text = "\n".join(points)
            prompt = f"Summarize the following research paper content into a single fluent paragraph:\n\n{combined_text}"

            try:
                response = llm.invoke(prompt)
                summary = response.strip()
            except Exception as e:
                print(f"[ERROR] LLM failed on paper '{title}': {e}")
                summary = combined_text  # fallback

            summaries.append(PaperSummary(title=title, url=url, summary=summary))

        return PaperSummaries(summaries=summaries)

    # --- Tool Decorator ---
    @tool
    def summarize_papers_tool(file_path: str = "ai-agent-output/scraped_papers.json") -> PaperSummaries:
        """
        Summarizes paper sections (abstract, intro, results, dataset) using an LLM from a scraped JSON file.
        """
        return summarize_papers_from_scraped_file(file_path=file_path, llm=llm)

    # --- Summarization Agent ---
    summarization_agent = Agent(
        role="Research Summarizer Agent",
        goal = "Summarize academic research papers into detailed, coherent paragraphs that highlight the main objectives, methodologies, technologies used, key findings, and results from all relevant sections.",
        backstory = "An AI-powered research assistant designed to leverage large language models (LLMs) for generating accurate, insightful, and engaging summaries of scholarly articles. It extracts and distills core ideas from each section—such as abstract, introduction, methodology, experiments, and conclusion—to provide a clear understanding of the paper’s contributions, applied technologies, and outcomes.",
        llm=llm,
        tools=[summarize_papers_tool],
        verbose=True
    )

    # --- Task Setup ---
    summarization_task = Task(
        description="Read from 'ai-agent-output/scraped_papers.json' and use LLM to summarize each paper into a well-structured paragraph. Use abstract, introduction, results, and dataset if available. If only abstract is found, still generate a strong summary.",
        expected_output="A JSON list of dictionaries with keys: title, url, summary",
        output_json=PaperSummaries,
        output_file=os.path.join("ai-agent-output", "final_summaries.json"),
        agent=summarization_agent
    )

    return summarization_agent,summarization_task



