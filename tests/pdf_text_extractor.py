from pathlib import Path
import pdfplumber


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from a generated PDF file.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    extracted_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

    return "\n".join(extracted_text)