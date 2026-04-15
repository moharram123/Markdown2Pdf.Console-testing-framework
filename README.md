# Automated Integration Test Suite for Markdown2Pdf.Console

This repository contains an automated integration test suite developed as part of the Bachelor thesis:

> **Design and Evaluation of an Automated Integration Test Suite for Markdown2Pdf.Console**

The goal of this project is to automatically validate PDF documents generated from Markdown and detect possible errors using a structured testing approach.

---

## Project Goal

Markdown2Pdf.Console is a tool that converts Markdown files into PDF documents.
In many real-world scenarios, these PDFs are not automatically tested, which can lead to unnoticed errors.

This project aims to:

* Automate the validation of generated PDFs
* Detect structural and content regressions
* Provide a simple baseline comparison mechanism
* Integrate testing into a CI/CD pipeline as a quality gate

---

## ⚙️ System Under Test

* **Tool:** Markdown2Pdf.Console
* **Version:** 2.0.2
* **Execution:** CLI (`dotnet tool run md2pdf`)

The converter itself is not modified. This repository focuses only on testing and validation.

---

## Project Structure

```text
markdown2pdf-quality-gate/
│
├── data/
│   ├── pilot/           # Valid test cases (control)
│   ├── regressions/     # Faulty test cases
│   └── baselines/       # Expected structures (JSON)
│
├── results/
│   ├── generated-pdfs/  # Generated PDF files
│   └── test-reports/    # HTML test reports
│
├── tests/
│   ├── test_auto_conversion.py
│   ├── system_adapter.py
│   ├── pdf_text_extractor.py
│   ├── baseline_comparator.py
│   └── evaluation_metrics.py
│
├── validation_rules/    # Validation logic
├── requirements.txt
└── pytest.ini
```

---

## Test Concept

The test suite validates four main elements in the generated PDFs:

* **Headings**
* **Tables**
* **Lists**
* **Code blocks**

###  Control Cases

Correct Markdown files that should pass all tests.

###  Regression Cases

Modified files containing intentional errors (e.g. missing elements).

This allows evaluation of how well the system detects errors.

---

## Baseline Mechanism

Each control file has a corresponding JSON baseline that defines the expected structure.

Example:

```json
{
  "headings": ["Features"],
  "lists": ["Item 1", "Item 2", "Item 3"]
}
```

During testing:

1. Markdown → PDF conversion
2. Text extraction from PDF
3. Comparison with baseline
4. Detection of differences

---

## How to Run

### 1. Install dependencies

```bash
dotnet tool restore
pip install -r requirements.txt
```

### 2. Run tests

```bash
pytest tests --html=results/test-reports/report.html --self-contained-html
```

---

##Output

After running tests:

* PDFs → `results/generated-pdfs/`
* Report → `results/test-reports/report.html`
* Metrics → CSV and JSON files

---

## Evaluation

The system supports basic evaluation metrics:

* Regression detection accuracy
* False positive rate
* Execution time
* Estimated time savings compared to manual validation

---

## CI/CD Integration

The project includes a GitHub Actions workflow that:

* Runs tests automatically
* Generates reports
* Fails the pipeline if tests fail

This acts as a **quality gate** for document generation.

---

## Limitations

* Validation is based on extracted text, not visual PDF layout
* Only selected Markdown features are tested
* Baseline approach is simplified

These limitations are discussed in the thesis.

---

## Author

* Assia Moharram

---

##  Note

This project is part of a Bachelor thesis in Business Informatics and follows a Design Science Research approach.
