# Automated Integration Test Framework for Markdown2Pdf.Console

This repository contains a testing framework developed as part of a Bachelor thesis:

> **Design and Evaluation of an Automated Integration Test Suite for Markdown2Pdf.Console**

The project focuses on validating PDF documents generated from Markdown and detecting structural issues in a consistent and reproducible way.

---

## Project Goal

Markdown2Pdf.Console is a command-line tool that converts Markdown files into PDF documents.

In many workflows, generated PDFs are not automatically checked, which means errors can go unnoticed.

The goal of this project is to:

* Automatically validate generated PDF documents
* Detect structural regressions (missing or broken elements)
* Use a simple baseline comparison approach
* Integrate testing into a CI/CD pipeline as a quality gate

---

## System Under Test

* **Tool:** Markdown2Pdf.Console
* **Version:** 2.0.2
* **Execution:** CLI (`dotnet tool run md2pdf`)

The converter is treated as an external system (black-box).
This repository focuses only on testing and validation.

---

## Project Structure

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
├── llm_experiments/    # Optional LLM experiment module (not part of core suite)
├── requirements.txt
├── requirements-llm.txt
└── pytest.ini
```

---

## Test Concept

The framework checks four basic Markdown structures in the generated PDFs:

* Headings
* Tables
* Lists
* Code blocks

### Control Cases

These are valid Markdown files that are expected to pass all tests.

### Regression Cases

These files contain intentional defects, for example:

* Missing heading
* Missing table row
* Missing list item
* Missing code block

This setup makes it easier to see whether the framework correctly detects errors.

---

## Baseline Mechanism

Each control file has a corresponding JSON file describing the expected structure.

Example:

```json
{
  "headings": ["Features"],
  "lists": ["Item 1", "Item 2", "Item 3"]
}
```

Test process:

1. Convert Markdown to PDF
2. Extract text from the PDF
3. Apply validation rules
4. Compare the result with the baseline
5. Store differences and results

The baseline approach is intentionally kept simple to keep the system understandable and manageable for a Bachelor thesis.

---
## Automated Quality Gate Setup

The framework includes an automated setup script to reduce manual effort:

```bash
python scripts/setup_quality_gate.py
```

This script:
- Creates required folder structure automatically
- Verifies all project dependencies are present
- Runs fully offline with no external dependencies
- Takes less than 1 second to complete

**No manual folder creation needed.**

## How the Quality Gate Works

The CI/CD pipeline is fully automated:

1. **Setup Phase** — Project structure is verified automatically via `setup_quality_gate.py`
2. **Test Phase** — Pytest runs all conversion and validation tests
3. **Report Phase** — Results are generated and uploaded as artifacts
4. **Quality Gate** — Pipeline fails if any regression is detected, blocking merges

Developers only need to push code. Everything else is automatic.

## Optional: LLM-Assisted Test Enrichment

For expanding the test dataset beyond manually written cases, optional LLM modules are available in `llm_experiments/`.

These can generate additional Markdown test cases and evaluate PDF readability:

```bash
pip install -r requirements-llm.txt
export OPENAI_API_KEY=your_key

# Generate synthetic Markdown test cases
python llm_experiments/generate_llm_test_cases.py --count 20

# Run tests on generated files
python llm_experiments/run_llm_test_suite.py

# Optional: Check PDF readability with LLM
python llm_experiments/llm_quality_check.py
```

**Important notes:**
- This is experimental and optional
- LLM outputs are non-deterministic
- Generated cases are for exploratory testing only
- The deterministic test suite is the authoritative baseline
- LLM is NOT part of the CI/CD pipeline
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

## Output

After running the tests:

* PDFs → `results/generated-pdfs/`
* Report → `results/test-reports/report.html`
* Metrics → `results/metrics/`
* Diff reports → `results/diffs/`

---

## Evaluation

The framework provides basic metrics that can be used in the thesis:

* Regression detection accuracy
* False positive rate
* Execution time
* Estimated time savings compared to manual validation

---

## CI/CD Integration

A GitHub Actions workflow is included.

It:

* Runs the tests on each push
* Generates reports
* Uploads results as artifacts

If tests fail, the workflow fails, which makes it usable as a simple quality gate.

---

## Core Automated Integration Test Suite

The main part of this project is a deterministic and fully offline test suite.
It does not require any API key or external service.

This is the central contribution of the thesis.

### How it works

1. Convert Markdown to PDF using the CLI tool
2. Extract text using `pdfminer.six`
3. Apply rule-based validation
4. Compare with baseline
5. Export results and metrics

---

## Optional LLM-Based Experiment

There is also a small experimental component located in `llm_experiments/`.

It uses the OpenAI API to check whether generated PDFs are readable and not corrupted.

This part is optional and not connected to the main test suite.
It does not affect test results or CI/CD status.

Because LLM outputs are not deterministic, this part is only used for exploration.

---

## Design Decisions

* The system uses a black-box approach
* Validation focuses on text structure, not layout
* The baseline mechanism is kept simple
* The focus is on stability and reproducibility

---

## Limitations

* No visual validation of PDFs
* Only a subset of Markdown features is tested
* Baseline comparison is simplified
* Results depend on text extraction quality

---

## Current Status

* Control and regression tests are working
* PDF validation is stable
* Metrics are generated
* CI/CD pipeline is running

---

## Author

Assia Moharram

---

## Note

This project is part of a Bachelor thesis in Business Informatics and follows a Design Science Research approach.
