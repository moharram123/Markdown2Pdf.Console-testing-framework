from pathlib import Path

import pytest

from tests.system_adapter import convert_markdown_to_pdf
from tests.pdf_text_extractor import extract_text_from_pdf


BASE_DIR = Path(__file__).resolve().parent.parent

CONTROL_DIR = BASE_DIR / "data" / "llm-generated" / "control"
REGRESSION_DIR = BASE_DIR / "data" / "llm-generated" / "regressions"
PDF_OUTPUT_DIR = BASE_DIR / "results" / "generated-pdfs" / "llm"


def markdown_files(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.md"))


def validate_pdf_structure(pdf_path: Path) -> None:
    text = extract_text_from_pdf(pdf_path)

    assert "Alice" in text
    assert "Bob" in text
    assert "Admin" in text

    assert "print" in text
    assert "console.log" in text

    # Flexible list validation:
    # The LLM may generate different list wording, so we check for several
    # common list-related indicators instead of one exact phrase.
    list_indicators = [
        "First item",
        "Second item",
        "Key Benefits",
        "Objectives",
        "priority",
        "features",
        "Goals",
    ]

    assert any(indicator.lower() in text.lower() for indicator in list_indicators)


@pytest.mark.parametrize("markdown_file", markdown_files(CONTROL_DIR))
def test_llm_control_cases_are_valid(markdown_file: Path) -> None:
    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_path = PDF_OUTPUT_DIR / f"{markdown_file.stem}.pdf"

    convert_markdown_to_pdf(markdown_file, pdf_path)

    assert pdf_path.exists(), f"PDF was not generated: {pdf_path}"

    validate_pdf_structure(pdf_path)


def test_llm_regression_cases_are_detected() -> None:
    files = markdown_files(REGRESSION_DIR)

    assert files, "No LLM regression files found."

    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    detected = 0

    for markdown_file in files:
        pdf_path = PDF_OUTPUT_DIR / f"{markdown_file.stem}.pdf"

        convert_markdown_to_pdf(markdown_file, pdf_path)

        try:
            validate_pdf_structure(pdf_path)
        except AssertionError:
            detected += 1

    detection_rate = detected / len(files)

    assert detection_rate >= 0.85, (
        f"Regression detection rate too low: {detected}/{len(files)} "
        f"({detection_rate:.2%})"
    )