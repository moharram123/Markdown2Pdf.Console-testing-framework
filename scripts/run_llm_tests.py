#!/usr/bin/env python3
"""
Runs the test suite against all LLM-generated Markdown documents.
Converts each .md in data/llm_generated/ to PDF via Markdown2Pdf.Console,
validates structural presence using the same 4 rule modules as the pilot suite,
and exports results to results/metrics/llm_results.csv and llm_metrics.json.
"""
import csv
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
PDF_DIR = RESULTS_DIR / "generated-pdfs"
METRICS_DIR = RESULTS_DIR / "metrics"
MD_DIR = DATA_DIR / "llm_generated"
BL_DIR = DATA_DIR / "baselines"
PDF_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIR.mkdir(parents=True, exist_ok=True)

from tests.system_adapter import convert_markdown_to_pdf
from tests.pdf_text_extractor import extract_text_from_pdf
from validation_rules.heading_rules import headings_are_valid
from validation_rules.table_rules import table_is_valid
from validation_rules.list_rules import list_is_valid
from validation_rules.codeblock_rules import codeblock_is_valid


def load_baseline_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_llm_test(md_file: Path, bl_file: Path) -> dict:
    pdf_path = PDF_DIR / f"{md_file.stem}.pdf"
    baseline_data = load_baseline_json(bl_file)
    start = time.perf_counter()
    conversion = convert_markdown_to_pdf(md_file, pdf_path)
    duration = time.perf_counter() - start
    if not conversion["success"]:
        return {
            "file": md_file.name,
            "should_pass": True,
            "actual_pass": False,
            "duration_seconds": round(duration, 4),
            "error": conversion["stderr"],
        }
    extracted = extract_text_from_pdf(pdf_path)
    heading_ok = headings_are_valid(extracted, baseline_data.get("headings", []))[0]
    table_ok = table_is_valid(extracted, baseline_data.get("tables", []))[0]
    list_ok = list_is_valid(extracted, baseline_data.get("lists", []))[0]
    code_ok = codeblock_is_valid(extracted, baseline_data.get("codeblocks", []))[0]
    overall = all([heading_ok, table_ok, list_ok, code_ok])
    return {
        "file": md_file.name,
        "should_pass": True,
        "actual_pass": overall,
        "duration_seconds": round(duration, 4),
        "details": {"heading_ok": heading_ok, "table_ok": table_ok, "list_ok": list_ok, "code_ok": code_ok},
    }


def save_llm_results(results: list[dict], out_csv: Path, out_json: Path):
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = ["file", "should_pass", "actual_pass", "duration_seconds", "heading_ok", "table_ok", "list_ok", "code_ok", "error"]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            writer.writerow({
                "file": r["file"],
                "should_pass": r["should_pass"],
                "actual_pass": r["actual_pass"],
                "duration_seconds": r["duration_seconds"],
                "heading_ok": r.get("details", {}).get("heading_ok"),
                "table_ok": r.get("details", {}).get("table_ok"),
                "list_ok": r.get("details", {}).get("list_ok"),
                "code_ok": r.get("details", {}).get("code_ok"),
                "error": r.get("error"),
            })
    total = len(results)
    passed = sum(1 for r in results if r["actual_pass"])
    accuracy = passed / total if total > 0 else 0.0
    avg_duration = sum(r["duration_seconds"] for r in results) / total if total > 0 else 0.0
    metrics = {"total_files": total, "passed": passed, "failed": total - passed, "accuracy": round(accuracy, 4), "avg_duration_seconds": round(avg_duration, 4)}
    out_json.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"\n=== LLM Test Suite Results ===")
    print(f"Total files:    {total}")
    print(f"Passed:         {passed}")
    print(f"Failed:         {total - passed}")
    print(f"Accuracy:       {accuracy * 100:.1f}%")
    print(f"Avg duration:   {avg_duration:.2f}s")
    print(f"Results saved:  {out_csv} and {out_json}")
    return metrics


def main():
    md_files = sorted(MD_DIR.glob("llm_*.md"), key=lambda p: int(p.stem.split("_")[1]))
    if not md_files:
        print("No llm-generated Markdown files found. Run scripts/llm_generate_tests.py first.")
        return
    results = []
    for i, md in enumerate(md_files, 1):
        bl = BL_DIR / (md.stem + ".json")
        print(f"[{i}/{len(md_files)}] {md.name}")
        results.append(run_llm_test(md, bl))
    save_llm_results(results, METRICS_DIR / "llm_results.csv", METRICS_DIR / "llm_metrics.json")


if __name__ == "__main__":
    main()
