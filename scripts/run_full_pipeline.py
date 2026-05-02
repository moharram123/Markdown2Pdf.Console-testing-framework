import subprocess
import sys


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

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()