#  Automated Integration Test Framework for Markdown2Pdf.Console

This repository contains a testing framework developed as part of a Bachelor thesis:

> **Design and Evaluation of an Automated Integration Test Suite for Markdown2Pdf.Console**

The project focuses on validating PDF documents generated from Markdown and detecting structural errors automatically using a reproducible testing approach.

---

##  Project Goal

Markdown2Pdf.Console is a command-line tool that converts Markdown files into PDF documents.

In many real-world workflows, generated PDFs are not automatically validated, which can lead to unnoticed errors.

This project aims to:

* Automate validation of generated PDF documents
* Detect structural regressions (missing or broken elements)
* Use a simple baseline comparison approach
* Integrate testing into a CI/CD pipeline as a quality gate

---

##  System Under Test

* **Tool:** Markdown2Pdf.Console
* **Version:** 2.0.2
* **Execution:** CLI (`dotnet tool run md2pdf`)

The original converter is treated as an **external system (black-box)**.
This repository focuses only on testing and validation.

---

##  Project Structure

```text
Markdown2Pdf.Console-testing-framework/
│
├── data/
│   ├── pilot/           # Valid Markdown files (control cases)
│   ├── regressions/     # Faulty Markdown files (regression cases)
│   └── baselines/       # Expected structures (JSON)
│
├── results/
│   ├── generated-pdfs/  # Generated PDF files
│   ├── test-reports/    # HTML reports
│   ├── metrics/         # Evaluation outputs
│   └── diffs/           # Per-case comparison results
│
├── tests/
│   ├── test_auto_conversion.py
│   ├── system_adapter.py
│   ├── pdf_text_extractor.py
│   ├── baseline_comparator.py
│   └── evaluation_metrics.py
│
├── validation_rules/    # Validation logic for structure checks
├── requirements.txt
└── pytest.ini
```

---

##  Test Concept

The framework validates four key Markdown structures in the generated PDFs:

* **Headings**
* **Tables**
* **Lists**
* **Code blocks**

###  Control Cases

Correct Markdown files that should pass all tests.

###  Regression Cases

Files containing intentional defects such as:

* Missing heading
* Missing table row
* Missing list item
* Missing code block

This allows evaluation of how well the framework detects errors.

---

## 📊 Baseline Mechanism

Each control file has a corresponding JSON baseline describing the expected structure.

Example:

```json
{
  "headings": ["Features"],
  "lists": ["Item 1", "Item 2", "Item 3"]
}
```

Test process:

1. Convert Markdown → PDF
2. Extract text from PDF
3. Apply validation rules
4. Compare extracted structure with baseline
5. Detect differences and store results

The baseline approach is intentionally simple to keep the system feasible for a Bachelor thesis.

---

##  How to Run

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

##  Output

After execution:

*  PDFs → `results/generated-pdfs/`
*  Report → `results/test-reports/report.html`
*  Metrics → `results/metrics/`
*  Diff reports → `results/diffs/`

---

##  Evaluation

The framework supports basic evaluation metrics:

* Regression detection accuracy
* False positive rate
* Execution time
* Estimated time savings compared to manual validation

These metrics are exported for use in the thesis evaluation chapter.

---

##  CI/CD Integration

The project includes a GitHub Actions workflow that:

* Runs tests automatically on each push
* Generates test reports
* Uploads results as artifacts

The pipeline acts as a **quality gate**:
if tests fail, the workflow fails.

---

##  Design Decisions

* A **black-box approach** is used because the converter is treated as an external CLI tool
* Validation focuses on **text structure**, not visual PDF layout
* The baseline mechanism is simplified for clarity and reproducibility
* The framework prioritizes **simplicity and stability** over complexity

---

##  Limitations

* No visual/layout validation of PDFs
* Limited set of Markdown features tested
* Baseline comparison is not fully comprehensive
* Results depend on text extraction accuracy

---

##  Current Status

* All control and regression tests are passing
* PDF validation is working correctly
* Metrics are generated for evaluation
* CI/CD pipeline is functional

---

##  Author

* Assia Moharram

---

## Note 

This project is part of a Bachelor thesis in Business Informatics and follows a Design Science Research approach.
