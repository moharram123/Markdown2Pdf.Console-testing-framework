"""
LLM-assisted Markdown test case generator.

This module generates additional Markdown control and regression test cases
based on external Markdown input documents. Generated files are integrated
into the automated test workflow for validation and execution.

Usage:
  pip install -r requirements-llm.txt
  $env:OPENAI_API_KEY = "your-key-here"
  python -m llm_assisted_generation.generate_llm_test_cases
"""

from pathlib import Path

from llm_assisted_generation.llm_client import get_llm_client
from llm_assisted_generation.llm_test_case_generator import generate_markdown_pair


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = BASE_DIR / "data" / "external-sources" / "downloaded"
OUTPUT_DIR = BASE_DIR / "data" / "llm-generated"

CONTROL_DIR = OUTPUT_DIR / "control"
REGRESSION_DIR = OUTPUT_DIR / "regressions"


def main() -> None:
    source_files = list(SOURCE_DIR.glob("*.md"))

    if not source_files:
        print("No Markdown source files found.")
        print(f"Expected files in: {SOURCE_DIR}")
        return

    CONTROL_DIR.mkdir(parents=True, exist_ok=True)
    REGRESSION_DIR.mkdir(parents=True, exist_ok=True)

    client = get_llm_client()

    print("Generating LLM-assisted Markdown test cases...")

    generated_count = 0

    for source_path in source_files:
        name = source_path.stem

        print(f"Processing: {name}")

        source_content = source_path.read_text(encoding="utf-8", errors="ignore")

        control_path = CONTROL_DIR / f"llm_{name}_control.md"
        regression_path = REGRESSION_DIR / f"llm_{name}_regression.md"

        if control_path.exists() and regression_path.exists():
            print(f"SKIPPED: {name} already generated")
            continue

        try:
            control, regression = generate_markdown_pair(client, source_content)
        except Exception as error:
            print(f"FAILED: {name} -> {error}")
            continue

        control_path.write_text(control, encoding="utf-8")
        regression_path.write_text(regression, encoding="utf-8")

        print(f"SAVED: {control_path}")
        print(f"SAVED: {regression_path}")

        generated_count += 2

    print(f"Done. Generated {generated_count} LLM-assisted test file(s).")


if __name__ == "__main__":
    main()