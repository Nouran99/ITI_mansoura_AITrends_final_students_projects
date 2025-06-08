import os
import streamlit as st
from typing import List
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process,LLM
from crewai.project import CrewBase, agent, task, crew
from Crew_folder.Tools.custom_tools import fetch_transcript,process_content ,export_content #,validate_url


# Load API key for initialize the llm.
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

@CrewBase
class YouTubeScriptCrew:
    agents: List[Agent]
    tasks: List[Task]



    @agent
    def transcript(self) -> Agent:
        return Agent(
            config=self.agents_config['transcript'],
            verbose=True,
            llm=llm,
            tools=[fetch_transcript]
        )

    @agent
    def instruction(self) -> Agent:
        return Agent(
            config=self.agents_config['instruction'],
            verbose=True,
            llm=llm,
            tools=[process_content]
            )

    @agent
    def export(self) -> Agent:
        return Agent(
            config=self.agents_config['export'],
            verbose=True,
            llm=llm,
            tools= [export_content]
        )
    
    @task
    def transcript_task(self) -> Task:
        return Task(
            config=self.tasks_config['transcript_task'],
            # context=[self.controller_task()]
        )

    @task
    def instruction_task(self) -> Task:
        return Task(
            config=self.tasks_config['instruction_task'],
            context=[self.transcript_task()]
        )

    @task
    def export_task(self) -> Task:
        return Task(
            config=self.tasks_config['export_task'],
            context=[self.instruction_task()],
            output_file='output/final_document.pdf'  
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )


if __name__ == "__main__":
    inputs = {
        "video_url": "https://youtu.be/QtEUU9ppVLU?si=5INC4JIclhAr8a3e",
        "instruction": "Summarize in 3 bullet points with emojis",
        "format": "pdf"  
    }

    crew = YouTubeScriptCrew().crew()
    result = crew.kickoff(inputs=inputs)

    print("\n===== YouTubeScriptCrew Results =====")

    if "validation" in result:
        print("\nValidation:")
        print(result["validation"])
        if result["validation"].get("status") == "error":
            exit()

    if "transcript" in result:
        print("\nTranscript (preview):")
        print(result["transcript"].get("transcript", "")[:300] + "...")

    if "processed" in result:
        print("\nProcessed Output:")
        print(result["processed"].get("processed_content", ""))

    if "export" in result:
        print("\nExport Result:")
        if result["export"]["status"] == "success":
            print("File saved at:", result["export"]["file_path"])
        else:
            print("Export error:", result["export"]["message"])
