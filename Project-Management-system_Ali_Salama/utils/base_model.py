from crewai import Agent, LLM
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["CREWAI_API_KEY"] = os.getenv("GEMINI_API_KEY")
# Instantiate the LLM
llm = LLM(
    model="gemini/gemini-2.5-flash-preview-04-17" ,
    temperature=0.7, 
)
