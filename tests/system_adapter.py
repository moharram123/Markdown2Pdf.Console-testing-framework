import os
import shutil
import subprocess
from pathlib import Path


def convert_markdown_to_pdf(markdown_path: Path, pdf_path: Path) -> None:
    """
    Convert a Markdown file to PDF using Markdown2Pdf.Console.

    The converter is first executed with only the input Markdown path.
    This is more stable with Markdown2Pdf.Console because it creates the PDF
    next to the Markdown file by default. The generated PDF is then moved to
    the requested output folder.
    """

    markdown_path = Path(markdown_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    command = os.getenv("M2P_COMMAND", "md2pdf")

    default_pdf_path = markdown_path.with_suffix(".pdf")

    if default_pdf_path.exists():
        default_pdf_path.unlink()

    result = subprocess.run(
        [command, str(markdown_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"PDF conversion failed for {markdown_path}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    if not default_pdf_path.exists():
        raise FileNotFoundError(
            f"Markdown2Pdf.Console did not create the expected PDF.\n"
            f"Expected: {default_pdf_path}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    shutil.move(str(default_pdf_path), str(pdf_path))

    if not pdf_path.exists():
        raise FileNotFoundError(f"Expected PDF was not created: {pdf_path}")