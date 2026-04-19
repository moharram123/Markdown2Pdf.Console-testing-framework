import os
import json
import csv
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "results" / "llm-generated-tests"


def generate_test_cases(markdown_path: Path) -> dict:
    """Ask LLM to generate test cases for a given markdown file."""
    markdown_content = markdown_path.read_text(encoding="utf-8")

    prompt = f"""
You are a test engineer. Analyze the following Markdown document and generate test cases for validating a PDF conversion.

For each test case, identify:
1. Expected headings that should appear in the PDF
2. Expected table content (key cell values)
3. Expected list items
4. Expected code block content

Return your answer as JSON in this exact format:
{{
  "file": "{markdown_path.name}",
  "expectations": {{
    "headings": ["heading1", "heading2"],
    "tables": ["cell_value1", "cell_value2"],
    "lists": ["item1", "item2"],
    "codeblocks": ["snippet1", "snippet2"]
  }}
}}

Markdown content:
{markdown_content[:3000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


def run_llm_test_generation():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    markdown_files = [
        DATA_DIR / "pilot" / "control_headings.md",
        DATA_DIR / "pilot" / "control_tables.md",
        DATA_DIR / "pilot" / "control_lists.md",
        DATA_DIR / "pilot" / "control_codeblocks.md",
        DATA_DIR / "experiments" / "experiment_kubernetes.md",
        DATA_DIR / "experiments" / "experiment_ohmyzsh.md",
        DATA_DIR / "experiments" / "experiment_fastapi.md",
    ]

    all_results = []

    for md_file in markdown_files:
        print(f"Generating tests for: {md_file.name}")
        result = generate_test_cases(md_file)
        all_results.append(result)

        output_path = OUTPUT_DIR / f"{md_file.stem}_llm_tests.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"  Saved to: {output_path}")

    summary_path = OUTPUT_DIR / "llm_generated_tests_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nDone! All results saved to: {OUTPUT_DIR}")
    return all_results


def save_llm_csv(comparison_results, output_dir):
    """Save LLM comparison results to CSV."""
    csv_path = output_dir / "llm_comparison.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "category", "manual_count", "llm_count", "matched", "coverage"])
        writer.writeheader()
        for file_result in comparison_results:
            for category, data in file_result["categories"].items():
                writer.writerow({
                    "file": file_result["file"],
                    "category": category,
                    "manual_count": data["manual_count"],
                    "llm_count": data["llm_count"],
                    "matched": len(data["matched"]),
                    "coverage": f"{int(data['coverage'] * 100)}%"
                })
    print(f"CSV saved to: {csv_path}")
    return csv_path


def save_llm_html(comparison_results, summary, output_dir):
    """Save LLM comparison results to HTML report."""
    html_path = output_dir / "llm_report.html"

    rows = ""
    for file_result in comparison_results:
        for category, data in file_result["categories"].items():
            coverage = int(data["coverage"] * 100)
            color = "#C6EFCE" if coverage >= 90 else "#FFC7CE"
            rows += f"""
            <tr style="background-color:{color}">
                <td>{file_result["file"]}</td>
                <td>{category}</td>
                <td>{data["manual_count"]}</td>
                <td>{data["llm_count"]}</td>
                <td>{len(data["matched"])}</td>
                <td>{coverage}%</td>
            </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>LLM Test Generation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2F75B6; }}
        h2 {{ color: #444; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th {{ background-color: #2F75B6; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border: 1px solid #ddd; }}
        .summary {{ background-color: #f0f0f0; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .badge {{ font-size: 2em; font-weight: bold; color: #2F75B6; }}
    </style>
</head>
<body>
    <h1>LLM-Assisted Test Generation Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <p>Total files analyzed: <strong>{summary["total_files"]}</strong></p>
        <p>Average coverage: <span class="badge">{int(summary["average_coverage"] * 100)}%</span></p>
        <p>{summary["conclusion"]}</p>
    </div>

    <h2>Detailed Results</h2>
    <table>
        <tr>
            <th>File</th>
            <th>Category</th>
            <th>Manual Count</th>
            <th>LLM Count</th>
            <th>Matched</th>
            <th>Coverage</th>
        </tr>
        {rows}
    </table>
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML saved to: {html_path}")
    return html_path


def compare_llm_vs_manual():
    """Compare LLM-generated tests vs manually written tests."""

    manual_tests = [
        {
            "file": "control_headings.md",
            "expectations": {
                "headings": ["Introduction", "Features"],
                "tables": [], "lists": [], "codeblocks": []
            }
        },
        {
            "file": "control_tables.md",
            "expectations": {
                "headings": [],
                "tables": ["Alice", "Bob", "Admin"],
                "lists": [], "codeblocks": []
            }
        },
        {
            "file": "control_lists.md",
            "expectations": {
                "headings": [], "tables": [],
                "lists": ["First item", "Second item", "Third item"],
                "codeblocks": []
            }
        },
        {
            "file": "control_codeblocks.md",
            "expectations": {
                "headings": [], "tables": [], "lists": [],
                "codeblocks": ["print("]
            }
        },
        {
            "file": "experiment_kubernetes.md",
            "expectations": {
                "headings": ["Kubernetes", "Introduction", "Features", "Usage", "Kubernetes Components", "Governance", "Community", "Support", "Security", "Architecture"],
                "tables": ["Alice", "Bob", "Carol", "Dave", "Admin"],
                "lists": ["First item", "Second item", "Third item", "Fourth item", "Fifth item", "Sixth item", "Seventh item", "Eighth item"],
                "codeblocks": ["print(", "def ", "console.log"]
            }
        },
        {
            "file": "experiment_ohmyzsh.md",
            "expectations": {
                "headings": ["Oh My Zsh", "Introduction", "Features", "Usage", "Plugin Reference Table", "Themes", "Configuration", "Community Contributors", "Getting Help", "Uninstalling"],
                "tables": ["Alice", "Bob", "Carol", "Dave", "Admin"],
                "lists": ["First item", "Second item", "Third item", "Fourth item", "Fifth item", "Sixth item", "Seventh item", "Eighth item"],
                "codeblocks": ["print(", "def ", "console.log"]
            }
        },
        {
            "file": "experiment_fastapi.md",
            "expectations": {
                "headings": ["FastAPI", "Introduction", "Features", "Usage", "Performance Benchmarks", "Sponsors Table", "Interactive Documentation", "Type System", "Security", "Community", "Contributors"],
                "tables": ["Alice", "Bob", "Carol", "Dave", "Admin"],
                "lists": ["First item", "Second item", "Third item", "Fourth item", "Fifth item", "Sixth item", "Seventh item"],
                "codeblocks": ["print(", "def ", "console.log"]
            }
        },
    ]

    summary_path = OUTPUT_DIR / "llm_generated_tests_summary.json"
    with open(summary_path, "r", encoding="utf-8") as f:
        llm_tests = json.load(f)

    comparison_results = []

    for manual, llm in zip(manual_tests, llm_tests):
        file_comparison = {"file": manual["file"], "categories": {}}
        total_score = 0
        total_categories = 0

        for category in ["headings", "tables", "lists", "codeblocks"]:
            manual_items = set(manual["expectations"].get(category, []))
            llm_items_raw = [
                str(item) if not isinstance(item, str) else item
                for item in llm["expectations"].get(category, [])
]
            if len(manual_items) == 0:
                coverage = 1.0
                matched = []
                extra = llm_items_raw
            else:
                matched = [m for m in manual_items if any(m.lower() in l.lower() for l in llm_items_raw)]
                coverage = round(len(matched) / len(manual_items), 2)
                extra = [l for l in llm_items_raw if not any(m.lower() in l.lower() for m in manual_items)]

            file_comparison["categories"][category] = {
                "manual_count": len(manual_items),
                "llm_count": len(llm_items_raw),
                "matched": matched,
                "extra_llm_found": extra,
                "coverage": coverage
            }

            total_score += coverage
            total_categories += 1

        file_comparison["overall_coverage"] = round(total_score / total_categories, 2)
        comparison_results.append(file_comparison)

    avg_coverage = round(sum(r["overall_coverage"] for r in comparison_results) / len(comparison_results), 2)

    report = {
        "summary": {
            "total_files": len(comparison_results),
            "average_coverage": avg_coverage,
            "conclusion": "LLM-generated tests cover {}% of manually written tests on average".format(int(avg_coverage * 100))
        },
        "file_results": comparison_results
    }

    report_path = OUTPUT_DIR / "comparison_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n=== LLM vs Manual Test Comparison ===")
    print(f"Files compared: {report['summary']['total_files']}")
    print(f"Average coverage: {int(avg_coverage * 100)}%")
    for r in comparison_results:
        print(f"  {r['file']}: {int(r['overall_coverage'] * 100)}% coverage")
    print(f"\nReport saved to: {report_path}")

    save_llm_csv(comparison_results, OUTPUT_DIR)
    save_llm_html(comparison_results, report["summary"], OUTPUT_DIR)

    return report


if __name__ == "__main__":
    run_llm_test_generation()
    compare_llm_vs_manual()