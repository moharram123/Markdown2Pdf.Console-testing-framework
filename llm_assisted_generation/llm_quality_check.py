from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CONTROL_DIR = BASE_DIR / "data" / "llm-generated" / "control"
REGRESSION_DIR = BASE_DIR / "data" / "llm-generated" / "regressions"


def has_heading(content: str) -> bool:
    return any(line.strip().startswith("#") for line in content.splitlines())


def has_table(content: str) -> bool:
    return "|" in content and "Name" in content and "Role" in content


def has_list(content: str) -> bool:
    return any(line.strip().startswith(("-", "*")) for line in content.splitlines())


def has_code_block(content: str) -> bool:
    return "```" in content


def check_control_file(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8", errors="ignore")
    errors = []

    if not has_heading(content):
        errors.append("missing heading")

    if not has_table(content):
        errors.append("missing table")

    if not has_list(content):
        errors.append("missing list")

    if not has_code_block(content):
        errors.append("missing code block")

    return errors


def run_quality_check() -> bool:
    control_files = sorted(CONTROL_DIR.glob("*.md"))
    regression_files = sorted(REGRESSION_DIR.glob("*.md"))

    if not control_files:
        print("No LLM control files found.")
        return False

    if not regression_files:
        print("No LLM regression files found.")
        return False

    success = True

    print("Running LLM-generated file quality check...")

    for file in control_files:
        errors = check_control_file(file)

        if errors:
            success = False
            print(f"FAILED: {file.name} -> {errors}")
        else:
            print(f"PASSED: {file.name}")

    print(f"Control files: {len(control_files)}")
    print(f"Regression files: {len(regression_files)}")

    return success


def main() -> None:
    if not run_quality_check():
        raise SystemExit(1)


if __name__ == "__main__":
    main()