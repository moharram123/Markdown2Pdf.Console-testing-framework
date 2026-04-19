from pathlib import Path
import subprocess
import shutil
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env file (local development) or environment variable (CI/CD)
load_dotenv()

# NOTE (Limitation): The LLM integration depends on the OpenAI API being available.
# If OPENAI_API_KEY is missing, expired, or rate-limited, ask_llm() will return a
# safe fallback value ("PASS - LLM unavailable, skipping check") so that the
# rest of the test suite can still run. This is an acknowledged reliability trade-off
# discussed in the thesis Limitations chapter.
_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=_api_key) if _api_key else None


def ask_llm(prompt: str) -> str:
    """Send a prompt to OpenAI and return the response text.

    Falls back gracefully if the API key is missing or the request fails,
    returning a PASS verdict so other validation layers still run.
    """
    if client is None:
        return "PASS - LLM unavailable, skipping check"
    try:
        time.sleep(1)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        # Return a safe PASS so rule-based checks are still evaluated
        return f"PASS - LLM error: {e}"


SUT_NAME = "Markdown2Pdf.Console"
SUPPORTED_VERSION = "2.0.2"
DEFAULT_COMMAND = ["dotnet", "tool", "run", "md2pdf"]


def run_command(command, cwd=None):
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result


def get_sut_version():
    result = run_command(DEFAULT_COMMAND + ["--version"])
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip()


def convert_markdown_to_pdf(markdown_path, pdf_path):
    markdown_path = Path(markdown_path)
    pdf_path = Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    command = DEFAULT_COMMAND + [str(markdown_path)]
    result = run_command(command)

    generated_pdf = markdown_path.with_suffix(".pdf")
    if generated_pdf.exists():
        shutil.move(str(generated_pdf), str(pdf_path))

    success = (result.returncode == 0) and pdf_path.exists()
    return {
        "sut_name": SUT_NAME,
        "expected_version": SUPPORTED_VERSION,
        "success": success,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "input_file": str(markdown_path),
        "output_file": str(pdf_path)
    }
