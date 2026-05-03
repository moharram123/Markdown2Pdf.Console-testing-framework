import os
from pathlib import Path

from tests.system_adapter import convert_markdown_to_pdf
from tests.pdf_text_extractor import extract_text_from_pdf


BASE_DIR = Path(__file__).resolve().parent.parent

CONTROL_DIR = BASE_DIR / "data" / "llm-generated" / "control"
REGRESSION_DIR = BASE_DIR / "data" / "llm-generated" / "regressions"


def get_run_mode() -> str:
    return "dynamic" if os.getenv("CLEAN_RUN", "false").lower() == "true" else "static"


PDF_OUTPUT_DIR = BASE_DIR / "results" / "generated-pdfs" / get_run_mode()


def markdown_files(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.md"))


def validate_pdf_structure(pdf_path: Path) -> None:
    text = extract_text_from_pdf(pdf_path)
    normalized_text = text.lower()

    assert "alice" in normalized_text
    assert "bob" in normalized_text
    assert "admin" in normalized_text

    assert "print" in normalized_text
    assert "console.log" in normalized_text

    list_indicators = [
        "first item",
        "second item",
        "key benefits",
        "objectives",
        "priority",
        "features",
        "goals",
        "guidelines",
        "steps",
        "requirements",
        "workflow",
        "tasks",
        "benefits",
        "components",
        "development",
        "setup",
        "installation",
        "configuration",
        "overview",
        "usage",
        "example",
    ]

    assert any(indicator in normalized_text for indicator in list_indicators), (
        f"No list-like structure detected in {pdf_path.name}"
    )


def test_llm_control_cases_are_valid() -> None:
    files = markdown_files(CONTROL_DIR)

    assert files, "No LLM control files found."

    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    passed = 0
    failed = []

    for markdown_file in files:
        pdf_path = PDF_OUTPUT_DIR / f"{markdown_file.stem}.pdf"

        convert_markdown_to_pdf(markdown_file, pdf_path)

        try:
            assert pdf_path.exists()
            assert pdf_path.stat().st_size > 0
            validate_pdf_structure(pdf_path)
            passed += 1
        except AssertionError as error:
            failed.append((markdown_file.name, str(error)))

    pass_rate = passed / len(files)

    assert pass_rate >= 0.90, (
        f"Control validation pass rate too low: "
        f"{passed}/{len(files)} passed ({pass_rate:.2%}). "
        f"Failed cases: {failed}"
    )


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