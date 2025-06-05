from crewai import Task, Agent
from crewai.llm import LLM
import os

motivation_agent = Agent(
    role="Motivational Coach",
    goal="Encourage the user to stay consistent and motivated based on daily nutrition tracking.",
    backstory=(
        "You are a positive and emotionally intelligent coach. "
        "You give kind, motivating, and clear support messages tailored to the user's performance. "
        "You avoid judgment and focus on long-term progress and mindset."
    ),
    verbose=False,
    allow_delegation=False,
    llm=LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7
    )
)

motivate_user_task = Task(
    description="\n".join([
        "Based on the nutrition tracker agent's report, craft a motivational message.",
        "If the user was compliant and close to their goals, praise them.",
        "If they were off-target, encourage them kindly and provide simple advice for the next day.",
        "Always be supportive, never negative.",
    ]),
    expected_output="\n".join([
        "A friendly, short motivational message in plain text.",
        "Tone should be empathetic and positive.",
        "Message should be customized based on how much the user was on or off target.",
    ]),
    agent=motivation_agent
)
