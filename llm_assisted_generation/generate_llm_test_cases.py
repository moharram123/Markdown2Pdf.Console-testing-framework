"""
Generate LLM-assisted Markdown test cases.

This script takes external Markdown files as input and uses an LLM to
automatically generate control (valid) and regression (faulty) test cases.

Each source file produces multiple variants to increase test coverage.
"""

from pathlib import Path

from llm_assisted_generation.llm_client import get_llm_client
from llm_assisted_generation.llm_test_case_generator import generate_markdown_pair


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = BASE_DIR / "data" / "external-sources" / "downloaded"

OUTPUT_DIR = BASE_DIR / "data" / "llm-generated"
CONTROL_DIR = OUTPUT_DIR / "control"
REGRESSION_DIR = OUTPUT_DIR / "regressions"


# 🔥 Increase this to control number of test cases
VARIANTS_PER_SOURCE = 3


def main() -> None:
    source_files = sorted(SOURCE_DIR.glob("*.md"))

    if not source_files:
        print("No Markdown source files found.")
        print(f"Expected files in: {SOURCE_DIR}")
        return

    CONTROL_DIR.mkdir(parents=True, exist_ok=True)
    REGRESSION_DIR.mkdir(parents=True, exist_ok=True)

    client = get_llm_client()

    print("=" * 60)
    print("LLM TEST GENERATION")
    print("=" * 60)

    print(f"Sources found: {len(source_files)}")
    print(f"Variants per source: {VARIANTS_PER_SOURCE}")
    print(f"Expected total files: {len(source_files) * VARIANTS_PER_SOURCE * 2}")
    print()

    generated_count = 0
    skipped_count = 0

    for source_path in source_files:
        source_name = source_path.stem

        print(f"\nProcessing source: {source_name}")

        source_content = source_path.read_text(encoding="utf-8", errors="ignore")

        # 🔁 Generate multiple variants
        for variant in range(1, VARIANTS_PER_SOURCE + 1):
            case_name = f"{source_name}_v{variant}"

            control_path = CONTROL_DIR / f"llm_{case_name}_control.md"
            regression_path = REGRESSION_DIR / f"llm_{case_name}_regression.md"

            # Skip already generated files
            if control_path.exists() and regression_path.exists():
                skipped_count += 2
                print(f"  SKIPPED: {case_name}")
                continue

            print(f"  Generating variant {variant}...")

            try:
                control, regression = generate_markdown_pair(
                    client=client,
                    source_content=source_content,
                    variant_number=variant,
                )
            except Exception as error:
                print(f"  FAILED: {case_name} -> {error}")
                continue

            # Save files
            control_path.write_text(control, encoding="utf-8")
            regression_path.write_text(regression, encoding="utf-8")

            generated_count += 2

            print(f"  SAVED: {control_path.name}")
            print(f"  SAVED: {regression_path.name}")

    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    print(f"New files generated: {generated_count}")
    print(f"Files skipped (already exist): {skipped_count}")
    print(f"Control folder: {CONTROL_DIR}")
    print(f"Regression folder: {REGRESSION_DIR}")


if __name__ == "__main__":
    main()