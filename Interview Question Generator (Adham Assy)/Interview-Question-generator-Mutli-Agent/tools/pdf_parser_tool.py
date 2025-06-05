# tools/pdf_parser_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, PrivateAttr
from typing import Type
import fitz  # PyMuPDF

class PDFParserArgs(BaseModel):
    """Input schema for PDFParserTool."""
    file_path: str

class PDFParserTool(BaseTool):
    name: str = "PDFParserTool"
    description: str = "Extracts text from a PDF resume file."
    args_schema: Type[PDFParserArgs] = PDFParserArgs
    
    def _run(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            doc = fitz.open(file_path)
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"

    def _arun(self, file_path: str) -> str:
        """Run the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")