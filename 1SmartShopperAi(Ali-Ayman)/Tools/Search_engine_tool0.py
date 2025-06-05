from crewai.tools import tool
from tavily import TavilyClient
import os


search_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def search_engine_tool(query: str):
    """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
    return search_client.search(query)