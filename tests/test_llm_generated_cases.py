import csv
import os
import time
from pathlib import Path

from tests.system_adapter import convert_markdown_to_pdf
from tests.pdf_text_extractor import extract_text_from_pdf


BASE_DIR = Path(__file__).resolve().parent.parent

CONTROL_DIR = BASE_DIR / "data" / "llm-generated" / "control"
REGRESSION_DIR = BASE_DIR / "data" / "llm-generated" / "regressions"

RUN_MODE = "dynamic" if os.getenv("CLEAN_RUN", "false").lower() == "true" else "static"

PDF_OUTPUT_DIR = BASE_DIR / "results" / "generated-pdfs" / RUN_MODE
METRICS_DIR = BASE_DIR / "results" / "metrics"
METRICS_FILE = METRICS_DIR / f"test_case_results_{RUN_MODE}.csv"


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

    assert any(indicator in normalized_text for indicator in list_indicators)


def write_result(row: dict) -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    file_exists = METRICS_FILE.exists()

    with METRICS_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "mode",
                "file",
                "case_type",
                "expected_result",
                "actual_result",
                "duration_sec",
                "status",
                "message",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def reset_metrics_file() -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    if METRICS_FILE.exists():
        METRICS_FILE.unlink()


def test_llm_control_cases_are_valid() -> None:
    reset_metrics_file()

    files = markdown_files(CONTROL_DIR)
    assert files, "No LLM control files found."

    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    passed = 0
    failed = []

    for markdown_file in files:
        start = time.perf_counter()
        pdf_path = PDF_OUTPUT_DIR / f"{markdown_file.stem}.pdf"

        status = "PASS"
        message = ""

        try:
            convert_markdown_to_pdf(markdown_file, pdf_path)

            assert pdf_path.exists()
            assert pdf_path.stat().st_size > 0

            validate_pdf_structure(pdf_path)

            actual_result = True
            passed += 1

        except AssertionError as error:
            actual_result = False
            status = "FAIL"
            message = str(error)
            failed.append(markdown_file.name)

        duration = round(time.perf_counter() - start, 4)

        write_result(
            {
                "mode": RUN_MODE,
                "file": markdown_file.name,
                "case_type": "control",
                "expected_result": True,
                "actual_result": actual_result,
                "duration_sec": duration,
                "status": status,
                "message": message,
            }
        )

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
        start = time.perf_counter()
        pdf_path = PDF_OUTPUT_DIR / f"{markdown_file.stem}.pdf"

        status = "PASS"
        message = ""

        try:
            convert_markdown_to_pdf(markdown_file, pdf_path)
            validate_pdf_structure(pdf_path)

            actual_result = True

        except AssertionError as error:
            actual_result = False
            detected += 1
            message = str(error)

        duration = round(time.perf_counter() - start, 4)

        # For regression files, detection means the test should fail structurally.
        expected_result = False
        detected_correctly = actual_result == expected_result

        if not detected_correctly:
            status = "FAIL"

        write_result(
            {
                "mode": RUN_MODE,
                "file": markdown_file.name,
                "case_type": "regression",
                "expected_result": expected_result,
                "actual_result": actual_result,
                "duration_sec": duration,
                "status": status,
                "message": message,
            }
        )

    detection_rate = detected / len(files)

    assert detection_rate >= 0.85, (
        f"Regression detection rate too low: {detected}/{len(files)} "
        f"({detection_rate:.2%})"
    )