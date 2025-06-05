
from crewai import Task, Agent
from crewai.llm import LLM
import os

tracker_agent = Agent(
    role="Nutrition Tracker",
    goal="Analyze user's actual intake and activity vs. planned intake to evaluate daily goal compliance.",
    backstory=(
        "You are a precise health auditor. Your role is to evaluate if the user followed the meal plan, "
        "met calorie/macro goals, and burned enough calories. You help users understand their performance "
        "and guide them with recommendations for better adherence."
    ),
    verbose=False,
    allow_delegation=False,
    llm=LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )
)

evaluate_nutrition_task = Task(
    description="\n".join([
        "Evaluate user's actual food intake and activity versus the planned meal plan.",
        "Inputs include:",
        "- planned_intake: list of meals with 'name', 'calories', 'protein_g', 'carbs_g', 'fats_g'",
        "- actual_intake: same structure based on what the user actually ate",
        "- burned_calories: calories burned by the user via activity or exercise.",
        "Steps:",
        "- Compare actual vs planned for each macro and total calories.",
        "- Compute net difference and determine whether user met the nutritional goal.",
        "- Consider activity: net calories = intake - burned",
        "- If significantly under or over, flag it.",
        "- Output a daily report."
    ]),
    expected_output="\n".join([
        "A JSON object like:",
        "{",
        "  'compliance_score': '85%',",
        "  'status': 'Partially met goals',",
        "  'macro_gaps': {",
        "    'calories': -150,",
        "    'protein_g': -10,",
        "    'carbs_g': +5,",
        "    'fats_g': -8",
        "  },",
        "  'recommendations': [",
        "    'Increase protein intake with a snack or shake',",
        "    'Reduce simple carbs at lunch',",
        "    'Try to meet calorie target to avoid under-fueling'",
        "  ]",
        "}"
    ]),
    agent=tracker_agent
)
