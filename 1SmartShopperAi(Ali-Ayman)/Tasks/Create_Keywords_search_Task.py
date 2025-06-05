# tasks/keywords_search_task.py
from crewai import Task
from typing import List
from pydantic import BaseModel, Field
import os


def create_keywords_search_task(
    product_name: str,
    websites_list: str,
    country_name: str,
    no_keywords: int,
    language: str,
    search_queries_recommendation_agent
):
    class DynamicSuggestedSearchQueries(BaseModel):
        queries: List[str] = Field(
            ..., 
            title="Suggested search queries to be passed to the search engine",
            min_items=3,
            max_items=no_keywords
        )

    # Define output path relative to this file
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data'))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "step_1_suggested_search_queries.json")

    return Task(
        description="\n".join([
            f"Rankyx aims to find **{product_name}** with a focus on value-for-money options.",
            f"Search should target the following websites: {websites_list}.",
            f"Locate **all relevant product listings** available online to enable comprehensive price and feature comparison.",
            f"Only include products that are sold in **{country_name}**.",
            f"Generate up to **{no_keywords}** highly specific search queries.",
            f"Queries must be composed in **{language}**.",
            "Include specific **brands, product types, or technologies**  avoid vague or generic terms.",
            "Make sure queries lead to **e-commerce product pages** directly, excluding blogs, news articles, or category hubs."
        ]),
        expected_output="A JSON object containing a list of relevant and highly specific search queries.",
        output_json=DynamicSuggestedSearchQueries,
        output_file=output_path,
        agent=search_queries_recommendation_agent
    )
