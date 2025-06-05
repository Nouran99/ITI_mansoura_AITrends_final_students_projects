# tasks/keywords_search_task.py

"""
Keyword Search Task Module

This module defines a CrewAI task that utilizes a search engine agent
to retrieve product data from e-commerce websites based on multiple search queries.
"""

from crewai import Task
from typing import List
from pydantic import BaseModel, Field
import os


def search_engine_task(score_th: float, Search_engine_agent) -> Task:
    """
    Creates a Task for performing e-commerce product search using a search engine agent.

    Args:
        score_th (float): Confidence score threshold to filter search results.
        Search_engine_agent: The CrewAI agent responsible for executing the search task.

    Returns:
        Task: A CrewAI Task object configured to perform the search and store results.
    """

    class SingleSearchResult(BaseModel):
        title: str
        url: str = Field(..., title="The page URL")
        content: str
        score: float
        search_query: str

    class AllSearchResults(BaseModel):
        results: List[SingleSearchResult]

    # Define output directory and path
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data'))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "step_2_suggested_search.json")

    return Task(
        description="\n".join([
            "Your task is to perform product searches using a list of suggested queries.",
            "For each query, gather search results from different websites.",
            "Focus only on single-product e-commerce pages (e.g., Amazon product pages, Walmart listings).",
            f"Discard any result with a confidence score below ({score_th}).",
            "Avoid suspicious, spammy, or non-ecommerce links.",
            "The goal is to collect reliable product information to support price comparison across sources."
        ]),
        expected_output="A JSON object containing the search results.",
        output_json=AllSearchResults,
        output_file=output_path,
        agent=Search_engine_agent
    )
