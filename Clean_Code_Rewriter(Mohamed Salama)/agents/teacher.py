# agents/teacher.py
import os
from crewai import Agent, LLM
from langchain_google_genai import ChatGoogleGenerativeAI

def create_educator_agent(gemini_model):
    # Using Gemini instead of XAI for consistency
    # gemini_llm = LLM(
    #     model="gemini/gemini-1.5-pro",
    #     api_key=os.getenv("GOOGLE_API_KEY"),
    #     temperature=0.7
    # )


    educator_agent = Agent(
        role="Clean Code Educator",
        goal="\n".join([
            "You are a Clean Code Educator. Based on the issues found in the code analysis,",
            "provide educational content about clean code principles and best practices.",
            "",
            "**REQUIRED OUTPUT FORMAT:**",
            "**CLEAN CODE LESSONS:**",
            "1. **[Issue Type]**: [Brief explanation of the principle]",
            "2. **Best Practice**: [How to avoid this issue]",
            "",
            "Keep explanations concise and practical."
        ]),
        
        backstory="""You are an experienced software engineering mentor who specializes 
        in teaching clean code principles. You excel at explaining complex concepts 
        in simple, practical terms.""",
        
        llm=gemini_model.get_llm(),
        verbose=False,
        allow_delegation=False,
        )
    
    return educator_agent