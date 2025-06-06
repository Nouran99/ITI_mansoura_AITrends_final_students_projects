import os
import re
from fpdf import FPDF
from docx import Document
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai.tools import tool

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")



@tool
def validate_url(url: str) -> dict:
    """
    Validates a YouTube video URL and returns the cleaned URL if valid.

    **Input:**
    - url (str): A raw YouTube video URL provided by the user.

    **Output:**
    - dict:
        - status (str): "success" if the URL is valid, "error" otherwise.
        - video_url (str, optional): The cleaned/valid YouTube URL.
        - message (str, optional): Error message if validation fails.

    **Behavior:**
    - Accepts standard and shortened YouTube URL formats.
    - Rejects malformed or non-YouTube URLs.

    **Valid formats:**
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID

    **Example:**
    >>> validate_url("https://www.youtube.com/watch?v=ABC123xyz78")
    {
        "status": "success",
        "video_url": "https://www.youtube.com/watch?v=ABC123xyz78"
    }
    """
    pattern = re.compile(
        r'^(https?://)?(www\.|m\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}(\?.*)?(&.*)?$'
    )
    if pattern.match(url):
        return {"status": "success", "video_url": url}
    return {
        "status": "error",
        "message": "Invalid YouTube URL. Valid formats:\n"
                   "- https://www.youtube.com/watch?v=VIDEO_ID\n"
                   "- https://youtu.be/VIDEO_ID"
    }


@tool
def fetch_transcript(video_url: str) -> dict:
    """
    Fetches the transcript of a YouTube video using its URL.

    **Input:**
    - video_url (str): A valid YouTube video URL.

    **Output:**
    - dict:
        - status (str): "success" if the transcript is retrieved, "error" otherwise.
        - script (str, optional): The full transcript text of the video.
        - message (str, optional): Error message if transcript extraction fails.

    **Behavior:**
    - Extracts the video ID from the YouTube URL.
    - Uses YouTubeTranscriptApi to retrieve the transcript.
    - Returns the full transcript as a plain string (no timestamps).

    **Example:**
    >>> fetch_transcript("https://youtu.be/ABC123xyz78")
    {
        "status": "success",
        "script": "Welcome to the video. Today we will talk about..."
    }
    """
    try:
        video_id = re.search(r'(?:v=|/)([\w-]{11})', video_url).group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item["text"] for item in transcript])    
        return {"status": "success", "script": text}
    
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch transcript: {str(e)}"}

    
@tool
def process_content(text: str, instruction: str) -> dict:
    """
    Processes content using Gemini LLM based on a user-provided instruction.

    **Inputs:**
    - text (str): The transcript or original content to process.
    - instruction (str): A custom instruction, e.g., "summarize", "translate", "extract keywords".

    **Output:**
    - dict:
        - status (str): "success" or "error"
        - processed_content (str, optional): The transformed content.
        - message (str, optional): Error message if processing fails.

    **Example:**
    >>> process_content(text="...", instruction="Summarize the content")
    {
        "status": "success",
        "processed_content": "This video is about..."
    }
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.5
        )
        response = llm.invoke(f"Original content:\n{text}\n\nInstruction: {instruction}")
        return {"status": "success", "processed_content": response.content}
    except Exception as e:
        return {"status": "error", "message": f"Processing failed: {str(e)}"}


@tool
def export_content(content: str, format: str) -> dict:
    """
    Exports processed content to a file in either PDF or Word format.

    **Inputs:**
    - content (str): The content to export (processed text).
    - format (str): Export format — "pdf" or "word".

    **Output:**
    - dict:
        - status (str): "success" or "error"
        - file_path (str, optional): Path to the exported file.
        - message (str, optional): Error message if export fails.

    **Example:**
    >>> export_content(content="Final script...", format="pdf")
    {
        "status": "success",
        "file_path": "output/output.pdf"
    }
    """
    try:
        os.makedirs("output", exist_ok=True)
        if format.lower() == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, content)
            output_path = "output/output.pdf"
            pdf.output(output_path)
        elif format.lower() == "word":
            doc = Document()
            doc.add_paragraph(content)
            output_path = "output/output.docx"
            doc.save(output_path)
        else:
            raise ValueError("Unsupported format. Use 'pdf' or 'word'.")
        return {"status": "success", "file_path": output_path}
    except Exception as e:
        return {"status": "error", "message": f"Export failed: {str(e)}"}