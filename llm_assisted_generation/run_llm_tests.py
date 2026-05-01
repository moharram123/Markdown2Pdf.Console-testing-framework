import subprocess
import sys


def run(command: str) -> None:
    print(f"\nRunning: {command}")
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    run("python -m llm_assisted_generation.fetch_external_markdown")
    run("python -m llm_assisted_generation.generate_llm_test_cases")
    run("python -m llm_assisted_generation.llm_quality_check")
    run(
        "pytest tests/test_llm_generated_cases.py -v "
        "--html=results/test-reports/llm-report.html "
        "--self-contained-html"
    )


if __name__ == "__main__":
    main()