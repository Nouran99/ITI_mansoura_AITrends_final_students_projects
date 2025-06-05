import os
import json
from typing import List, Union
from pydantic import BaseModel, Field, ValidationError
from scrapegraph_py import Client
from crewai.tools import tool

# ==========================
# Environment Setup
# ==========================

SCRAPEGRAPH_API_KEY = os.getenv("ScrapeGraphAI_KEY")
scrapegraph = Client(api_key=SCRAPEGRAPH_API_KEY)

# ==========================
# Data Models
# ==========================

class ProductSpec(BaseModel):
    specification_name: str
    specification_value: str

class SingleExtractedProduct(BaseModel):
    page_url: str = Field(..., title="The original url of the product page")
    product_title: str = Field(..., title="The title of the product")
    product_image_url: str = Field(default=None, title="The url of the product image")
    product_url: str = Field(..., title="The url of the product")
    product_current_price: float = Field(..., title="The current price of the product")
    product_original_price: float = Field(default=None, title="The original price of the product before discount")
    product_discount_percentage: float = Field(default=None, title="The discount percentage of the product")

    product_specs: List[ProductSpec] = Field(
        default_factory=list, 
        title="The specifications of the product", 
        max_items=5
    )

    agent_recommendation_rank: int = Field(
        default=1, 
        ge=1, 
        le=5, 
        title="Rank of the product in recommendation list"
    )
    agent_recommendation_notes: List[str] = Field(
        default_factory=list, 
        title="Notes about product recommendation"
    )

class AllExtractedProducts(BaseModel):
    products: List[SingleExtractedProduct]

# ==========================
# Web Scraping Tool
# ==========================

@tool
def web_scraping_tool(page_url: str):
    """
    AI-powered web scraping tool to extract detailed product information from e-commerce pages.

    This tool uses ScrapegraphAI to intelligently scrape and extract structured product details 
    from various e-commerce websites. It aims to collect comprehensive information about 
    a specific product, including:
    - Product title
    - URL
    - Price details
    - Product specifications
    - Recommendation insights

    Args:
        page_url (str): The full URL of the product page to be scraped.

    Returns:
        dict: A dictionary containing extracted product information, structured according 
              to the SingleExtractedProduct model. Returns an empty product list if 
              scraping fails.

    Example:
        web_scraping_tool("https://www.example.com/product/iphone-15")
    
    Raises:
        Various exceptions related to network, parsing, or API issues may be handled internally.
    """
    try:
        # Attempt to scrape the webpage
        details = scrapegraph.smartscraper(
            website_url=page_url,
            user_prompt="Extract ```json\n" + json.dumps(SingleExtractedProduct.model_json_schema()) + "```\n From the web page"
        )

        # Handle potential string or dictionary responses
        if isinstance(details, str):
            try:
                details = json.loads(details)
            except json.JSONDecodeError:
                return {"products": []}

        # Validate and convert to expected format
        try:
            validated_product = SingleExtractedProduct(**details)
            return {
                "products": [validated_product.model_dump()]
            }
        except ValidationError:
            # Log validation errors if needed
            return {"products": []}

    except Exception as e:
        # Log the exception
        print(f"Scraping error for {page_url}: {e}")
        return {"products": []}