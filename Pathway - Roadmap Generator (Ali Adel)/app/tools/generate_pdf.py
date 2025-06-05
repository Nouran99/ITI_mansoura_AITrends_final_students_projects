from fpdf import FPDF

def export_pdf(plan_text: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    lines = plan_text.strip().splitlines()

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("**"):  # Title or emphasis
            text = stripped.strip("*").strip()
            pdf.set_font("Arial", "B", size=14)
            pdf.cell(0, 10, txt=text, ln=True)

        elif stripped.startswith("*"):  # Bullet point
            text = "- " + stripped.lstrip("*").strip()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=text)

        elif stripped == "":  # Blank line
            pdf.ln()

        else:  # Normal text
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=stripped)

    return pdf.output(dest="S").encode("latin1")
