import pdfplumber

def extract_text_from_pdf(filepath: str) -> str:
    """Extract plain text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = f"Error reading PDF: {str(e)}"
    return text.strip()
