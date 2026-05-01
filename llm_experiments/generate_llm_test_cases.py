"""
Optional OpenAI-based Markdown test case generator.

This script is experimental and is not part of the core pytest suite or CI/CD
pipeline. It generates additional Markdown control and regression cases that
can be reviewed before being added to the main dataset.

Usage:
  pip install -r requirements-llm.txt
  $env:OPENAI_API_KEY = "your-key-here"
  python -m llm_experiments.generate_llm_test_cases
"""

import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: Install LLM dependencies first:")
    print("pip install -r requirements-llm.txt")
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "experiments"
OUTPUT_DIR = BASE_DIR / "data" / "llm-generated"

CONTROL_DIR = OUTPUT_DIR / "control"
REGRESSION_DIR = OUTPUT_DIR / "regressions"

SOURCE_FILES = {
    "kubernetes": SOURCE_DIR / "experiment_kubernetes.md",
    "fastapi": SOURCE_DIR / "experiment_fastapi.md",
    "ohmyzsh": SOURCE_DIR / "experiment_ohmyzsh.md",
}


def build_prompt(source_content: str) -> str:
    return f"""
Generate two Markdown test cases based on the source document.

Return exactly this format:

---CONTROL---
<valid markdown>

---REGRESSION---
<faulty markdown>

Requirements for CONTROL:
- It must be valid Markdown.
- It must contain at least 5 headings using #, ##, or ###.
- It must contain one table with the columns Name and Role.
- The table must include the rows Alice, Bob, Carol, Dave, and Admin.
- It must contain one bullet list with at least 6 items.
- The bullet list must include:
  First item, Second item, Third item, Fourth item, Fifth item, Sixth item.
- It must contain one Python code block with print( and def.
- It must contain one JavaScript code block with console.log.

Requirements for REGRESSION:
- It must be similar to the control case.
- It must contain exactly one intentional structural defect.
- Choose one of these defects:
  missing heading, missing table row, missing list item, or missing code block.
- Do not explain the defect inside the Markdown file.

Output only the requested format. Do not add explanations.

Source document:
---
{source_content}
---
""".strip()


def split_response(content: str) -> tuple[str, str]:
    if "---CONTROL---" not in content or "---REGRESSION---" not in content:
        raise ValueError("LLM response does not contain the expected markers.")

    control_part = content.split("---CONTROL---", 1)[1].split("---REGRESSION---", 1)[0]
    regression_part = content.split("---REGRESSION---", 1)[1]

    control = control_part.strip()
    regression = regression_part.strip()

    if not control or not regression:
        raise ValueError("Generated control or regression content is empty.")

    return control, regression


def generate_case(client: OpenAI, source_content: str) -> tuple[str, str]:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate Markdown test cases. Output only the requested raw Markdown format.",
            },
            {
                "role": "user",
                "content": build_prompt(source_content),
            },
        ],
        temperature=0.4,
        max_tokens=2500,
    )

    content = response.choices[0].message.content.strip()
    return split_response(content)


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("OPENAI_API_KEY is not set.")
        print("This script is optional and was skipped.")
        print('Run: $env:OPENAI_API_KEY = "your-key-here"')
        return

    CONTROL_DIR.mkdir(parents=True, exist_ok=True)
    REGRESSION_DIR.mkdir(parents=True, exist_ok=True)

    client = OpenAI(api_key=api_key)

    print("Generating optional LLM-assisted Markdown test cases...")

    generated_count = 0

    for name, source_path in SOURCE_FILES.items():
        if not source_path.exists():
            print(f"SKIPPED: {source_path.name} not found")
            continue

        source_content = source_path.read_text(encoding="utf-8")

        try:
            control, regression = generate_case(client, source_content)
        except Exception as error:
            print(f"FAILED: {name} -> {error}")
            continue

        control_path = CONTROL_DIR / f"llm_{name}_control.md"
        regression_path = REGRESSION_DIR / f"llm_{name}_regression.md"

        control_path.write_text(control, encoding="utf-8")
        regression_path.write_text(regression, encoding="utf-8")

        print(f"SAVED: {control_path}")
        print(f"SAVED: {regression_path}")

        generated_count += 2

    print(f"Done. Generated {generated_count} optional LLM test file(s).")
    print("Review generated files before adding them to the core dataset.")


if __name__ == "__main__":
    main()