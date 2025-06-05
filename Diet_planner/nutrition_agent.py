from tools import SpoonacularTool
from crewai import Task, Agent
from crewai.llm import LLM
import os

nutrition_agent = Agent(
    role="Nutrition Expert",
    goal=(
        "Generate personalized, balanced meal plans for users based on their health goals, "
        "calorie needs, and dietary preferences."
    ),
    backstory=(
        "You are a nutrition expert trained on dietary guidelines, fitness coaching knowledge, "
        "and real meal plan data. You pull live data via external APIs like Spoonacular to enhance accuracy."
    ),
    verbose=False,
    allow_delegation=False,
    tools=[SpoonacularTool()],
    llm=LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )
)

generate_meal_plan_task = Task(
    description="\n".join([
        "Create a daily meal plan with 3 main meals (breakfast, lunch, dinner) and 2 snacks,",
        "based on the user's goal, target calories (e.g. 1800 kcal), and diet type (e.g. keto, vegetarian).",
        "Each meal and snack should have a name, short description, estimated calories, and macro breakdown.",
        "Use Spoonacular API to fetch real recipes and nutritional data.",
        "Output should be structured and easy to read.",
        "Ensure the total daily calories are as close as possible to the target_calories.",
        "If initial choices are low, suggest calorie-dense options or more snacks.",
        "If not able to meet the exact target, suggest how to bridge the gap.",
        "Return the output as valid JSON only (use double quotes, no Python syntax)."
    ]),
    expected_output="\n".join([
        "A JSON list of dictionaries, where each dictionary represents a meal or snack.",
        "Each dictionary MUST contain the following keys: \"meal_type\", \"name\", \"description\", \"estimated_calories\", \"protein_g\", \"carbs_g\", \"fats_g\", \"recipe_link\".",
        "Ensure the output is ONLY the JSON list, with no surrounding text or formatting.",
        "The JSON should be directly parsable by json.loads() into a Python list of dictionaries suitable for pd.DataFrame()."
    ]),
    agent=nutrition_agent
)

