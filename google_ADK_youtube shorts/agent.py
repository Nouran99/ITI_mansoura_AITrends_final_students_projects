from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from .instructions import VISUAL_SUGGESTER_INSTRUCTION,SHORTS_CONTENT_ORCHESTRATOR_INSTRUCTION,SCRIPT_WRITER_INSTRUCTION

import os

try:
    from dotenv import load_dotenv
    load_dotenv()

    MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")
except ImportError:
    print("Warning: python-dotenv not installed. Ensure API key is set")
    MODEL_NAME = "gemini-2.0-flash"
    
# --- Sub Agent 1: Scriptwriter ---
scriptwriter_agent = LlmAgent(
    name="ShortsScriptwriter",
    model=MODEL_NAME,
    description="Generate a Script for the shorts",
    instruction=SCRIPT_WRITER_INSTRUCTION,
    #tools=[google_search],
    output_key="generated_script",  # Save result to state
)

# --- Sub Agent 2: Visualizer ---
visualizer_agent = LlmAgent(
    name="ShortsVisualizer",
    model=MODEL_NAME,
    instruction=VISUAL_SUGGESTER_INSTRUCTION,
    description="Generates visual concepts based on a provided script.",
    output_key="visual_concepts",  # Save result to state
)

# --- Sub Agent 3: Formatter ---
# This agent would read both state keys and combine into the final Markdown
formatter_agent = LlmAgent(
    name="ConceptFormatter",
    model=MODEL_NAME,
    instruction="""Combine the script from state['generated_script'] and the visual concepts from state['visual_concepts'] into the final Markdown format requested previously (Hook, Script & Visuals table, Visual Notes, CTA).""",
    description="Formats the final Short concept.",
    output_key="final_short_concept",
)


# --- Llm Agent Workflow ---
youtube_shorts_agent = LlmAgent(
    name="youtube_shorts_agent",
    model=MODEL_NAME,
    instruction=SHORTS_CONTENT_ORCHESTRATOR_INSTRUCTION,
    description="You are an agent that can write scripts, visuals and format youtube short videos. You have subagents that can do this",
    sub_agents=[scriptwriter_agent, visualizer_agent, formatter_agent],
    tools=[],
)


# --- Root Agent for the Runner ---
# The runner will now execute the workflow
root_agent = youtube_shorts_agent