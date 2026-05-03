import csv
import os
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_DIR = BASE_DIR / "results" / "metrics"

RUN_MODE = "dynamic" if os.getenv("CLEAN_RUN", "false").lower() == "true" else "static"

INPUT_CSV = METRICS_DIR / f"test_case_results_{RUN_MODE}.csv"
OUTPUT_FILE = METRICS_DIR / f"llm_metrics_{RUN_MODE}.xlsx"


def read_rows() -> list[dict]:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Metrics CSV not found: {INPUT_CSV}")

    with INPUT_CSV.open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def style_header(ws) -> None:
    fill = PatternFill("solid", fgColor="1F4E78")
    font = Font(color="FFFFFF", bold=True)

    for cell in ws[1]:
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center")


def auto_fit_columns(ws) -> None:
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)

        for cell in column:
            if cell.value is not None:
                max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[column_letter].width = min(max_length + 3, 45)


def add_borders(ws) -> None:
    thin = Side(style="thin", color="D9D9D9")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for row in ws.iter_rows():
        for cell in row:
            cell.border = border


def prepare_sheet(ws) -> None:
    style_header(ws)
    add_borders(ws)
    auto_fit_columns(ws)


def bool_value(value: str) -> bool:
    return str(value).lower() == "true"


def create_test_case_sheet(wb: Workbook, rows: list[dict]) -> None:
    ws = wb.active
    ws.title = "Test Cases"

    headers = [
        "mode",
        "file",
        "case_type",
        "expected_result",
        "actual_result",
        "duration_sec",
        "status",
        "message",
    ]

    ws.append(headers)

    for row in rows:
        ws.append(
            [
                row["mode"],
                row["file"],
                row["case_type"],
                row["expected_result"],
                row["actual_result"],
                float(row["duration_sec"]),
                row["status"],
                row["message"],
            ]
        )

    prepare_sheet(ws)


def create_summary_sheet(wb: Workbook, rows: list[dict]) -> dict:
    ws = wb.create_sheet("Summary")

    total = len(rows)
    passed = sum(1 for row in rows if row["status"] == "PASS")
    failed = total - passed

    control_rows = [row for row in rows if row["case_type"] == "control"]
    regression_rows = [row for row in rows if row["case_type"] == "regression"]

    control_passed = sum(1 for row in control_rows if row["status"] == "PASS")
    regression_detected = sum(
        1 for row in regression_rows
        if bool_value(row["actual_result"]) == bool_value(row["expected_result"])
    )

    total_duration = round(sum(float(row["duration_sec"]) for row in rows), 2)
    average_duration = round(total_duration / total, 2) if total else 0

    accuracy = round((passed / total) * 100, 2) if total else 0
    control_pass_rate = round((control_passed / len(control_rows)) * 100, 2) if control_rows else 0
    detection_rate = round((regression_detected / len(regression_rows)) * 100, 2) if regression_rows else 0

    false_positives = sum(
        1 for row in control_rows
        if row["status"] == "FAIL"
    )

    false_positive_rate = round((false_positives / len(control_rows)) * 100, 2) if control_rows else 0

    metrics = {
        "Total Test Cases": total,
        "Passed Test Cases": passed,
        "Failed Test Cases": failed,
        "Control Cases": len(control_rows),
        "Regression Cases": len(regression_rows),
        "Control Pass Rate (%)": control_pass_rate,
        "Regression Detection Rate (%)": detection_rate,
        "False Positive Rate (%)": false_positive_rate,
        "Overall Accuracy (%)": accuracy,
        "Total Duration (sec)": total_duration,
        "Average Duration per Test (sec)": average_duration,
    }

    ws.append(["Metric", "Value"])

    for key, value in metrics.items():
        ws.append([key, value])

    prepare_sheet(ws)

    chart = BarChart()
    chart.title = "LLM Pipeline Summary"
    chart.y_axis.title = "Value"
    chart.x_axis.title = "Metric"

    data = Reference(ws, min_col=2, min_row=1, max_row=12)
    categories = Reference(ws, min_col=1, min_row=2, max_row=12)

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)
    chart.height = 10
    chart.width = 18

    ws.add_chart(chart, "D2")

    return metrics


def create_status_chart_sheet(wb: Workbook, rows: list[dict]) -> None:
    ws = wb.create_sheet("Pass Fail Chart")

    passed = sum(1 for row in rows if row["status"] == "PASS")
    failed = len(rows) - passed

    ws.append(["Status", "Count"])
    ws.append(["Passed", passed])
    ws.append(["Failed", failed])

    prepare_sheet(ws)

    chart = PieChart()
    chart.title = "Passed vs Failed Test Cases"

    data = Reference(ws, min_col=2, min_row=2, max_row=3)
    categories = Reference(ws, min_col=1, min_row=2, max_row=3)

    chart.add_data(data)
    chart.set_categories(categories)

    ws.add_chart(chart, "D2")


def create_duration_sheet(wb: Workbook, rows: list[dict]) -> None:
    ws = wb.create_sheet("Duration Analysis")

    ws.append(["file", "duration_sec"])

    for row in rows:
        ws.append([row["file"], float(row["duration_sec"])])

    prepare_sheet(ws)

    chart = BarChart()
    chart.title = "Duration per Test Case"
    chart.y_axis.title = "Seconds"
    chart.x_axis.title = "Test Case"

    data = Reference(ws, min_col=2, min_row=1, max_row=len(rows) + 1)
    categories = Reference(ws, min_col=1, min_row=2, max_row=len(rows) + 1)

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)
    chart.height = 12
    chart.width = 24

    ws.add_chart(chart, "D2")


def main() -> None:
    rows = read_rows()

    wb = Workbook()

    create_test_case_sheet(wb, rows)
    create_summary_sheet(wb, rows)
    create_status_chart_sheet(wb, rows)
    create_duration_sheet(wb, rows)

    wb.save(OUTPUT_FILE)

    print(f"Excel metrics report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()