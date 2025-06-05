import requests
from crewai.tools import BaseTool
import os
class SpoonacularTool(BaseTool):
    # Add type annotations (str) to name and description
    name: str = "Spoonacular Recipe Finder"
    description: str = "Fetches real meals and nutrition info based on ingredients or meal name"

    def _run(self, query: str) -> str:
        api_key = os.getenv("SPOONACULAR_API_KEY")
        if not api_key:
            return "Spoonacular API key not found in environment variables."

        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "query": query,
            "number": 5,  # get 5 recipes to increase variety
            "addRecipeNutrition": True,
            "addRecipeInformation": True,
            "apiKey": api_key
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return f"Error from Spoonacular API: {response.status_code}"

        data = response.json()
        results = data.get("results", [])
        if not results:
            return "No recipe found."

        recipes = []
        for recipe in results:
            nutrients = recipe.get("nutrition", {}).get("nutrients", [])

            def get_nutrient(name):
                for n in nutrients:
                    if n["name"].lower() == name.lower():
                        return n["amount"]
                return "N/A"

            recipes.append({
                "title": recipe.get("title"),
                "link": recipe.get("sourceUrl"),
                "calories": get_nutrient("Calories"),
                "protein": get_nutrient("Protein"),
                "carbs": get_nutrient("Carbohydrates"),
                "fats": get_nutrient("Fat")
            })

        # Returning a Python list of dictionaries as a string representation
        # This is to align with the expected_output format which avoids JSON formatting.
        # However, parsing this string later might be tricky.
        # A cleaner approach would be to return a JSON string and parse it.
        # Let's stick to the requested format for now.
        return str(recipes)
