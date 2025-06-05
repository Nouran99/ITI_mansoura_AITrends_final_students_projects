import re
from datetime import datetime
import html 
#import pdfkit


def html_file_generator(result):
    # Access the raw string output and then unescape HTML entities
    html_content = html.unescape(result.raw)

    # Define the output HTML file path
    output_html_file = "project_plan.html"

    # Save the HTML content to a file
    with open(output_html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return output_html_file

# def pdf_file_generator(result):

#     html_content = html_file_generator(result)
#     output_pdf_file = "project_plan.pdf"
#     # Provide path if not in PATH
#     # wkhtmltopdf neaded
#     config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

#     #pdfkit.from_string(html_content, output_pdf_file, configuration=config)
#     pdfkit.from_file(html_content, output_pdf_file, configuration=config)
#     return output_pdf_file