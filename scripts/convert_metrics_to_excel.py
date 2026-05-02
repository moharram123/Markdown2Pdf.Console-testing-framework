from pathlib import Path
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference


BASE_DIR = Path(__file__).resolve().parent.parent

CONTROL_DIR = BASE_DIR / "data" / "llm-generated" / "control"
REGRESSION_DIR = BASE_DIR / "data" / "llm-generated" / "regressions"
PDF_DIR = BASE_DIR / "results" / "generated-pdfs" / "llm"
METRICS_DIR = BASE_DIR / "results" / "metrics"

METRICS_DIR.mkdir(parents=True, exist_ok=True)


def count_files(folder: Path, pattern: str) -> int:
    if not folder.exists():
        return 0
    return len(list(folder.glob(pattern)))


def main():
    # 🔢 counts
    control_count = count_files(CONTROL_DIR, "*.md")
    regression_count = count_files(REGRESSION_DIR, "*.md")
    pdf_count = count_files(PDF_DIR, "*.pdf")

    # 🧪 عدلي حسب results ديالك
    pytest_total = 34
    pytest_passed = 33
    pytest_failed = 1

    regression_detected = 33
    regression_missed = 0

    detection_rate = round((regression_detected / regression_count) * 100, 2) if regression_count else 0

    # 📊 create Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Metrics"

    # headers
    ws.append(["Metric", "Value"])

    data = [
        ("Control Markdown Files", control_count),
        ("Regression Markdown Files", regression_count),
        ("Generated PDFs", pdf_count),
        ("Pytest Total", pytest_total),
        ("Pytest Passed", pytest_passed),
        ("Pytest Failed", pytest_failed),
        ("Regression Detected", regression_detected),
        ("Regression Missed", regression_missed),
        ("Detection Rate (%)", detection_rate),
    ]

    for row in data:
        ws.append(row)

    # 📊 create chart
    chart = BarChart()
    chart.title = "LLM Pipeline Results"
    chart.y_axis.title = "Value"
    chart.x_axis.title = "Metrics"

    data_ref = Reference(ws, min_col=2, min_row=1, max_row=len(data)+1)
    categories = Reference(ws, min_col=1, min_row=2, max_row=len(data)+1)

    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(categories)

    ws.add_chart(chart, "D2")

    # 💾 save
    excel_path = METRICS_DIR / "llm_metrics.xlsx"
    wb.save(excel_path)

    print(f"Excel saved: {excel_path}")


if __name__ == "__main__":
    main()