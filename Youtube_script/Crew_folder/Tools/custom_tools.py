import os
import time
import random
from fpdf import FPDF
from crewai import LLM
from docx import Document
from crewai.tools import tool
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Load environment first
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

llm = LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.7,
        )
   

@tool("Fetch YouTube Video Transcript")
def fetch_transcript(video_url: str) -> str:
    """
    Fetches the transcript for a given YouTube video URL, attempting to retrieve
    manually created or auto-generated captions in the specified languages.
    Implements rate limiting and retries on failure.

    Returns:
        str: The formatted transcript or an error message.
    """

    def extract_video_id(url: str) -> str:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                query_params = parse_qs(parsed_url.query)
                return query_params.get('v', [None])[0]
            elif parsed_url.path.startswith('/shorts/'):
                return parsed_url.path.split('/')[2]
        elif hostname == 'youtu.be':
            return parsed_url.path.lstrip('/')

        raise ValueError("Invalid YouTube URL format.")

    max_retries = 5
    languages = ['en', 'ar', 'en-US']

    video_id = extract_video_id(video_url)

    for attempt in range(max_retries):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try manually created transcripts
            for lang in languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    break
                except Exception:
                    continue
            else:
                # Fallback to auto-generated transcripts
                for lang in languages:
                    try:
                        transcript = transcript_list.find_generated_transcript([lang])
                        break
                    except Exception:
                        continue
                else:
                    return "❌ No transcript found for the specified languages."

            formatter = TextFormatter()
            formatted_transcript = formatter.format_transcript(transcript.fetch())
            final_transcript = formatted_transcript.replace("\n", " ") 
            return final_transcript

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️ Error: {e}. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                return f"❌ Failed to fetch transcript after {max_retries} attempts. Error: {str(e)}"

    
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

        response = llm.call(f"Original content:\n{text}\n\nInstruction: {instruction}")
        return {"status": "success", "processed_content": response}
    
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
    


# @tool
# def validate_url(url: str) -> dict:
#     """
#     Validates a YouTube video URL and returns the cleaned URL if valid.

#     **Input:**
#     - url (str): A raw YouTube video URL provided by the user.

#     **Output:**
#     - dict:
#         - status (str): "success" if the URL is valid, "error" otherwise.
#         - video_url (str, optional): The cleaned/valid YouTube URL.
#         - message (str, optional): Error message if validation fails.

#     **Behavior:**
#     - Accepts standard and shortened YouTube URL formats.
#     - Rejects malformed or non-YouTube URLs.

#     **Valid formats:**
#     - https://www.youtube.com/watch?v=VIDEO_ID
#     - https://youtu.be/VIDEO_ID

#     **Example:**
#     >>> validate_url("https://www.youtube.com/watch?v=ABC123xyz78")
#     {
#         "status": "success",
#         "video_url": "https://www.youtube.com/watch?v=ABC123xyz78"
#     }
#     """
#     pattern = re.compile(
#         r'^(https?://)?(www\.|m\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}(\?.*)?(&.*)?$'
#     )
#     if pattern.match(url):
#         return {"status": "success", "video_url": url}
#     return {
#         "status": "error",
#         "message": "Invalid YouTube URL. Valid formats:\n"
#                    "- https://www.youtube.com/watch?v=VIDEO_ID\n"
#                    "- https://youtu.be/VIDEO_ID"
#     }

# @tool
# def fetch_transcript(video_url: str) -> dict:
#     """
#     Fetches the transcript of a YouTube video using its URL.

#     **Input:**
#     - video_url (str): A valid YouTube video URL.

#     **Output:**
#     - dict:
#         - status (str): "success" if the transcript is retrieved, "error" otherwise.
#         - script (str, optional): The full transcript text of the video.
#         - message (str, optional): Error message if transcript extraction fails.

#     **Behavior:**
#     - Extracts the video ID from the YouTube URL.
#     - Uses YouTubeTranscriptApi to retrieve the transcript.
#     - Returns the full transcript as a plain string (no timestamps).

#     **Example:**
#     >>> fetch_transcript("https://youtu.be/ABC123xyz78")
#     {
#         "status": "success",
#         "script": "Welcome to the video. Today we will talk about..."
#     }
#     """
#     try:
#         video_id = re.search(r'(?:v=|/)([\w-]{11})', video_url).group(1)
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         text = " ".join([item["text"] for item in transcript])    
#         return {"status": "success", "script": text}
    
#     except Exception as e:
#         return {"status": "error", "message": f"Failed to fetch transcript: {str(e)}"}
