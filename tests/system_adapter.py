from pathlib import Path
import subprocess
import shutil
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask_llm(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """Send a prompt to Groq and return the response text."""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    return response.choices[0].message.content


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