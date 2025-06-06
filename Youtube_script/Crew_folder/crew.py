import os
from typing import List
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from langchain_google_genai import ChatGoogleGenerativeAI
from Tools.custom_tools import fetch_transcript,validate_url,process_content,export_content


# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")


@CrewBase
class YouTubeScriptCrew:
    agents: List[Agent]
    tasks: List[Task]

    @agent
    def controller(self) -> Agent:
        return Agent(
            config=self.agents_config['controller'],
            llm=None,
            verbose=True,
            tools=[validate_url]
        )

    @agent
    def transcript(self) -> Agent:
        return Agent(
            config=self.agents_config['transcript'],
            verbose=True,
            tools=[fetch_transcript]
        )

    @agent
    def instruction(self) -> Agent:
        return Agent(
            config=self.agents_config['instruction'],
            llm=ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=GEMINI_API_KEY
            ),
            verbose=True,
            tools=[process_content]
        )

    @agent
    def export(self) -> Agent:
        return Agent(
            config=self.agents_config['export'],
            verbose=True,
            tools= [export_content]
        )

    @task
    def controller_task(self) -> Task:
        return Task(
            config=self.tasks_config['controller_task']
        )

    @task
    def transcript_task(self) -> Task:
        return Task(
            config=self.tasks_config['transcript_task'],
            context=[self.controller_task()]
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
        "video_url": "https://www.youtube.com/ّwatch?v=ZVzgfmqCwGQ",
        "instruction": "Summarize in 3 bullet points",
        "export_format": "pdf"  
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
