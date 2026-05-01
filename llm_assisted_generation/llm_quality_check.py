from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONTROL_DIR = BASE_DIR / "data" / "llm-generated" / "control"
REGRESSION_DIR = BASE_DIR / "data" / "llm-generated" / "regressions"


def contains_heading(content: str) -> bool:
    return any(line.startswith("#") for line in content.splitlines())


def contains_table(content: str) -> bool:
    return "|" in content and "Name" in content and "Role" in content


def contains_list(content: str) -> bool:
    return any(line.strip().startswith(("-", "*")) for line in content.splitlines())


def contains_code_block(content: str) -> bool:
    return "```" in content


def check_control_file(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8", errors="ignore")
    errors = []

    if not contains_heading(content):
        errors.append("missing heading")

    if not contains_table(content):
        errors.append("missing table")

    if not contains_list(content):
        errors.append("missing list")

    if not contains_code_block(content):
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

    print("Running LLM quality check...")

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


if __name__ == "__main__":
    passed = run_quality_check()

    if not passed:
        raise SystemExit(1)