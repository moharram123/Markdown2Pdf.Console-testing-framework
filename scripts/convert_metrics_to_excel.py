from pathlib import Path
import csv
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "results" / "llm-quality-check" / "llm_verdicts.csv"
OUTPUT_DIR = BASE_DIR / "results" / "metrics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def auto_size_columns(ws):
    for col in ws.columns:
        max_length = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "LLM Results"

    # Read CSV
    if not INPUT_CSV.exists():
        print("CSV not found:", INPUT_CSV)
        return

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row_idx, row in enumerate(reader, start=1):
            ws.append(row)

            # Bold header
            if row_idx == 1:
                for col_idx in range(1, len(row) + 1):
                    ws.cell(row=row_idx, column=col_idx).font = Font(bold=True)

    # Auto resize
    auto_size_columns(ws)

    # Create summary
    total = ws.max_row - 1
    passed = sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r[2] == "True")
    failed = total - passed

    ws_summary = wb.create_sheet("Summary")

    ws_summary.append(["Metric", "Value"])
    ws_summary.append(["Total Tests", total])
    ws_summary.append(["Passed", passed])
    ws_summary.append(["Failed", failed])

    # Bold header
    for cell in ws_summary[1]:
        cell.font = Font(bold=True)

    # Chart
    chart = BarChart()
    chart.title = "Test Results Overview"
    chart.y_axis.title = "Count"
    chart.x_axis.title = "Metrics"

    data = Reference(ws_summary, min_col=2, min_row=2, max_row=4)
    categories = Reference(ws_summary, min_col=1, min_row=2, max_row=4)

    chart.add_data(data)
    chart.set_categories(categories)

    ws_summary.add_chart(chart, "D2")

    #Save
    output_file = OUTPUT_DIR / "llm_detailed_results.xlsx"
    wb.save(output_file)

    print(f"Excel saved: {output_file}")


if __name__ == "__main__":
    main()