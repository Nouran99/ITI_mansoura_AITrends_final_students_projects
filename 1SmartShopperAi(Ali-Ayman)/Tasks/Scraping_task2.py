from crewai import Task
import os
from pydantic import BaseModel, Field
from typing import List
from Tools import Scraping_Tool1


def Scraping_task(top_recommendations_no: int, scraping_agent) -> Task:
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data'))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "step_3_scraping_results.json")

    class ScrapingResults(BaseModel):
        products: List[Scraping_Tool1.SingleExtractedProduct]

    return Task(
        description="\n".join([
            f"Extract product details from top {top_recommendations_no} e-commerce store URLs.",
            "Collect comprehensive product information.",
            "Ensure data integrity and completeness."
        ]),
        expected_output="A JSON object containing product details",
        output_json=ScrapingResults,  # Use the new model
        output_file=output_path,
        agent=scraping_agent
    )