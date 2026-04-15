from pathlib import Path
import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "experiments" / "llm"

PROMPT = """
Create one small Markdown test document for PDF conversion testing.
Requirements:
- include 2 headings
- include 1 small table with 2 rows
- include 1 bullet list with 3 items
- include 1 short code block
Return Markdown only.
"""


def generate_markdown_with_llm():
    if OpenAI is None:
        raise RuntimeError("openai package is not installed.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=PROMPT
    )
    return response.output_text.strip()


def save_generated_case(content, filename="llm_case_01.md"):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / filename
    file_path.write_text(content, encoding="utf-8")
    return file_path


if __name__ == "__main__":
    markdown = generate_markdown_with_llm()
    saved_path = save_generated_case(markdown)
    print(f"Saved generated file to: {saved_path}")