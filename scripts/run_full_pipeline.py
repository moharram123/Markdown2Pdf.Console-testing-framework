import shutil
import subprocess
import sys
from pathlib import Path


GENERATED_FOLDERS = [
    Path("data/external-sources"),
    Path("data/llm-generated"),
    Path("results"),
]


def clean_generated_outputs() -> None:
    """
    Remove generated input, output, and result folders before each pipeline run.

    This makes every execution start from a clean state:
    - new external Markdown files are downloaded
    - new LLM test cases are generated
    - new PDFs, reports, and Excel metrics are created
    """

    print("\n" + "=" * 60)
    print("Clean generated folders")
    print("=" * 60)

    for folder in GENERATED_FOLDERS:
        if folder.exists():
            shutil.rmtree(folder)
            print(f"Removed: {folder}")
        else:
            print(f"Skipped: {folder} does not exist")


def run_step(title: str, command: list[str]) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\nPipeline stopped at: {title}")
        sys.exit(result.returncode)


def main() -> None:
    print("=" * 60)
    print("FULL AUTOMATED LLM TESTING PIPELINE")
    print("=" * 60)

    clean_generated_outputs()

    run_step(
        "Download external Markdown sources",
        [sys.executable, "-m", "llm_assisted_generation.external_markdown"],
    )

    run_step(
        "Generate LLM-assisted control and regression test cases",
        [sys.executable, "-m", "llm_assisted_generation.generate_llm_test_cases"],
    )

    run_step(
        "Run LLM-generated file quality check",
        [sys.executable, "-m", "llm_assisted_generation.llm_quality_check"],
    )

    run_step(
        "Run LLM-generated pytest cases",
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_llm_generated_cases.py",
            "-v",
            "--html=results/test-reports/llm-report.html",
            "--self-contained-html",
        ],
    )

    run_step(
        "Generate Excel metrics",
        [sys.executable, "scripts/convert_metrics_to_excel.py"],
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()