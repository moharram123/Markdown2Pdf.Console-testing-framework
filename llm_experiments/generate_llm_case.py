# llm_experiments/generate_llm_case.py
"""
Optional LLM-based Markdown variant generator using Groq API.
Not part of the core pytest test suite.

Usage:
  pip install -r requirements-llm.txt
  $env:GROQ_API_KEY = 'your-key-here'
  python -m llm_experiments.generate_llm_case
"""
import os
import sys
from pathlib import Path

try:
    from groq import Groq
except ImportError:
    print("ERROR: Run: pip install groq  (or pip install -r requirements-llm.txt)")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = BASE_DIR / "data" / "experiments"
OUTPUT_DIR = BASE_DIR / "data" / "experiments" / "llm"

SOURCE_FILES = {
    "llm_kubernetes_variant.md": EXPERIMENTS_DIR / "experiment_kubernetes.md",
    "llm_fastapi_variant.md": EXPERIMENTS_DIR / "experiment_fastapi.md",
    "llm_ohmyzsh_variant.md": EXPERIMENTS_DIR / "experiment_ohmyzsh.md",
}


def build_prompt(source_content):
    return (
        "Generate a NEW Markdown variation of the document below.\n"
        "Requirements:\n"
        "- At least 5 headings using ## and ###\n"
        "- One table with columns Name and Role, rows: Alice, Bob, Carol, Dave, Admin\n"
        "- One bullet list with 6 items starting with: First item:, Second item:, "
        "Third item:, Fourth item:, Fifth item:, Sixth item:\n"
        "- One Python code block containing print( and def\n"
        "- One JavaScript code block containing console.log\n"
        "- Output only raw Markdown\n"
        "Original:\n---\n" + source_content + "\n---"
    )


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY is not set.")
        print("Run: $env:GROQ_API_KEY = 'your-key-here'")
        sys.exit(1)

    client = Groq(api_key=api_key)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating {len(SOURCE_FILES)} LLM variant files...")

    for output_filename, source_path in SOURCE_FILES.items():
        if not source_path.exists():
            print(f"  SKIPPED: {source_path.name} not found")
            continue

        source_content = source_path.read_text(encoding="utf-8")
        print(f"  Generating {output_filename}...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Output only raw Markdown."},
                {"role": "user", "content": build_prompt(source_content)},
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        content = response.choices[0].message.content.strip()
        output_path = OUTPUT_DIR / output_filename
        output_path.write_text(content, encoding="utf-8")
        print(f"  Saved: {output_path}")

    print(f"Done! {len(SOURCE_FILES)} variant(s) written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
