from pathlib import Path
import time
import pytest

from .system_adapter import convert_markdown_to_pdf, get_sut_version, SUPPORTED_VERSION
from .pdf_text_extractor import extract_text_from_pdf
from .baseline_comparator import load_baseline, compare_baseline, save_difference_report
from .evaluation_metrics import calculate_metrics, save_metrics_json, save_results_csv

from validation_rules.heading_rules import headings_are_valid
from validation_rules.table_rules import table_is_valid
from validation_rules.list_rules import list_is_valid
from validation_rules.codeblock_rules import codeblock_is_valid


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RESULTS_DIR = BASE_DIR / "results"
PDF_DIR = RESULTS_DIR / "generated-pdfs"
REPORT_DIR = RESULTS_DIR / "test-reports"
METRICS_DIR = RESULTS_DIR / "metrics"
DIFF_DIR = RESULTS_DIR / "diffs"


def build_extracted_structure(extracted_text):
    return {
        "headings": [item for item in [
            "Introduction", "Features", "Usage",
            "Kubernetes", "Kubernetes Components", "Governance", "Community",
            "Support", "Security", "Architecture",
            "Oh My Zsh", "Plugin Reference Table", "Themes", "Configuration",
            "Community Contributors", "Getting Help", "Uninstalling",
            "FastAPI", "Performance Benchmarks", "Sponsors Table",
            "Interactive Documentation", "Type System", "Contributors"
        ] if item in extracted_text],

        "tables": [item for item in [
            "Alice", "Bob", "Admin", "Carol", "Dave"
        ] if item in extracted_text],

        "lists": [item for item in [
            "First item", "Second item", "Third item",
            "Fourth item", "Fifth item", "Sixth item",
            "Seventh item", "Eighth item"
        ] if item in extracted_text],

        "codeblocks": [item for item in [
            "print(", "def ", "console.log"
        ] if item in extracted_text]
    }


def run_case(markdown_file, baseline_file, expectations, should_pass):
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_DIR.mkdir(parents=True, exist_ok=True)

    pdf_path = PDF_DIR / f"{markdown_file.stem}.pdf"

    start = time.perf_counter()
    conversion = convert_markdown_to_pdf(markdown_file, pdf_path)
    duration = time.perf_counter() - start

    if not conversion["success"]:
        pytest.fail(f"Conversion failed for {markdown_file.name}: {conversion['stderr']}")

    extracted_text = extract_text_from_pdf(pdf_path)

    heading_ok, missing_headings = headings_are_valid(extracted_text, expectations.get("headings", []))
    table_ok, missing_tables = table_is_valid(extracted_text, expectations.get("tables", []))
    list_ok, missing_lists = list_is_valid(extracted_text, expectations.get("lists", []))
    code_ok, missing_code = codeblock_is_valid(extracted_text, expectations.get("codeblocks", []))

    extracted_structure = build_extracted_structure(extracted_text)
    baseline_data = load_baseline(baseline_file)
    comparison = compare_baseline(baseline_data, extracted_structure)

    report_path = DIFF_DIR / f"{markdown_file.stem}_diff.json"
    save_difference_report(comparison, report_path)

    overall_valid = all([heading_ok, table_ok, list_ok, code_ok, comparison["overall_match"]])

    if should_pass and not overall_valid:
        pytest.fail(
            f"Control case failed for {markdown_file.name}. "
            f"Missing headings: {missing_headings}; "
            f"Missing tables: {missing_tables}; "
            f"Missing lists: {missing_lists}; "
            f"Missing code: {missing_code}"
        )

    if not should_pass and overall_valid:
        pytest.fail(f"Regression case unexpectedly passed: {markdown_file.name}")

    return {
        "file": markdown_file.name,
        "should_pass": should_pass,
        "actual_pass": overall_valid,
        "duration_seconds": round(duration, 4)
    }


def test_sut_version_is_available():
    version = get_sut_version()
    assert version == "unknown" or SUPPORTED_VERSION in version


TEST_CASES = [
    {
        "markdown": DATA_DIR / "pilot" / "control_headings.md",
        "baseline": DATA_DIR / "baselines" / "control_headings.json",
        "expectations": {"headings": ["Introduction", "Features"]},
        "should_pass": True
    },
    {
        "markdown": DATA_DIR / "pilot" / "control_tables.md",
        "baseline": DATA_DIR / "baselines" / "control_tables.json",
        "expectations": {"tables": ["Alice", "Bob", "Admin"]},
        "should_pass": True
    },
    {
        "markdown": DATA_DIR / "pilot" / "control_lists.md",
        "baseline": DATA_DIR / "baselines" / "control_lists.json",
        "expectations": {"lists": ["First item", "Second item", "Third item"]},
        "should_pass": True
    },
    {
        "markdown": DATA_DIR / "pilot" / "control_codeblocks.md",
        "baseline": DATA_DIR / "baselines" / "control_codeblocks.json",
        "expectations": {"codeblocks": ["print("]},
        "should_pass": True
    },
    {
        "markdown": DATA_DIR / "regressions" / "missing_heading.md",
        "baseline": DATA_DIR / "baselines" / "control_headings.json",
        "expectations": {"headings": ["Introduction", "Features"]},
        "should_pass": False
    },
    {
        "markdown": DATA_DIR / "regressions" / "missing_table_row.md",
        "baseline": DATA_DIR / "baselines" / "control_tables.json",
        "expectations": {"tables": ["Alice", "Bob", "Admin"]},
        "should_pass": False
    },
    {
        "markdown": DATA_DIR / "regressions" / "missing_list_item.md",
        "baseline": DATA_DIR / "baselines" / "control_lists.json",
        "expectations": {"lists": ["First item", "Second item", "Third item"]},
        "should_pass": False
    },
    {
        "markdown": DATA_DIR / "regressions" / "missing_codeblock.md",
        "baseline": DATA_DIR / "baselines" / "control_codeblocks.json",
        "expectations": {"codeblocks": ["print("]},
        "should_pass": False
    },
        {
        "markdown": DATA_DIR / "experiments" / "experiment_kubernetes.md",
        "baseline": DATA_DIR / "baselines" / "experiment_kubernetes.json",
        "expectations": {
            "headings": ["Kubernetes", "Introduction", "Features", "Usage", "Kubernetes Components", "Governance", "Community", "Support", "Security", "Architecture"],
            "tables": ["Alice", "Bob", "Carol", "Dave", "Admin"],
            "lists": ["First item", "Second item", "Third item", "Fourth item", "Fifth item", "Sixth item", "Seventh item", "Eighth item"],
            "codeblocks": ["print(", "def ", "console.log"]
        },
        "should_pass": True
    },
    {
        "markdown": DATA_DIR / "experiments" / "experiment_ohmyzsh.md",
        "baseline": DATA_DIR / "baselines" / "experiment_ohmyzsh.json",
        "expectations": {
            "headings": ["Oh My Zsh", "Introduction", "Features", "Usage", "Plugin Reference Table", "Themes", "Configuration", "Community Contributors", "Getting Help", "Uninstalling"],
            "tables": ["Alice", "Bob", "Carol", "Dave", "Admin"],
            "lists": ["First item", "Second item", "Third item", "Fourth item", "Fifth item", "Sixth item", "Seventh item", "Eighth item"],
            "codeblocks": ["print(", "def ", "console.log"]
        },
        "should_pass": True
    },
    {
        "markdown": DATA_DIR / "experiments" / "experiment_fastapi.md",
        "baseline": DATA_DIR / "baselines" / "experiment_fastapi.json",
        "expectations": {
            "headings": ["FastAPI", "Introduction", "Features", "Usage", "Performance Benchmarks", "Sponsors Table", "Interactive Documentation", "Type System", "Security", "Community", "Contributors"],
            "tables": ["Alice", "Bob", "Carol", "Dave", "Admin"],
            "lists": ["First item", "Second item", "Third item", "Fourth item", "Fifth item", "Sixth item", "Seventh item"],
            "codeblocks": ["print(", "def ", "console.log"]
        },
        "should_pass": True
    },

]


@pytest.mark.parametrize(
    "markdown_file, baseline_file, expectations, should_pass",
    [
        (case["markdown"], case["baseline"], case["expectations"], case["should_pass"])
        for case in TEST_CASES
    ]
)
def test_markdown_conversion_cases(markdown_file, baseline_file, expectations, should_pass):
    run_case(markdown_file, baseline_file, expectations, should_pass)

def test_export_metrics():
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    results = [
        run_case(
            case["markdown"],
            case["baseline"],
            case["expectations"],
            case["should_pass"]
        )
        for case in TEST_CASES
    ]

    metrics = calculate_metrics(results)
    save_results_csv(results, METRICS_DIR / "results.csv")
    save_metrics_json(metrics, METRICS_DIR / "metrics.json")

    assert (METRICS_DIR / "results.csv").exists()
    assert (METRICS_DIR / "metrics.json").exists()