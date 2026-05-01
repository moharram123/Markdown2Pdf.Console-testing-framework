# Automated Integration Test Framework for Markdown2Pdf.Console

This repository contains a testing framework developed as part of a Bachelor thesis: **Design and Evaluation of an Automated Integration Test Suite for Markdown2Pdf.Console**

The project focuses on validating PDF documents generated from Markdown and detecting structural issues in a consistent and reproducible way.

## Project Goal

Markdown2Pdf.Console is a command-line tool that converts Markdown files into PDF documents. In many workflows, generated PDFs are not automatically checked, which means errors can go unnoticed.

The goal of this project is to:
* Automatically validate generated PDF documents
* Detect structural regressions (missing or broken elements)
* Use a simple baseline comparison approach
* Integrate testing into a CI/CD pipeline as a quality gate

## System Under Test

* **Tool:** Markdown2Pdf.Console
* **Version:** 2.0.2
* **Execution:** CLI (`dotnet tool run md2pdf`)

The converter is treated as an external system (black-box). This repository focuses only on testing and validation.

## Project Structure

```
Markdown2Pdf.Console-testing-framework/
│
├── data/
│   ├── pilot/          # Valid Markdown files (control cases)
│   ├── regressions/    # Faulty Markdown files (regression cases)
│   └── baselines/      # Expected structures (JSON)
│
├── results/
│   ├── generated-pdfs/ # Generated PDF files
│   ├── test-reports/   # HTML reports
│   ├── metrics/        # Evaluation outputs
│   └── diffs/          # Per-case comparison results
│
├── tests/
│   ├── test_auto_conversion.py
│   ├── system_adapter.py
│   ├── pdf_text_extractor.py
│   ├── baseline_comparator.py
│   └── evaluation_metrics.py
│
├── validation_rules/            # Validation logic for structure checks
├── scripts/                     # Automation and setup scripts
├── llm_experiments/             # Optional LLM experiment module (not part of core suite)
├── requirements.txt
├── requirements-llm.txt
└── pytest.ini
```

## Test Concept

The framework checks four basic Markdown structures in the generated PDFs:
* Headings
* Tables
* Lists
* Code blocks

### Control Cases

Valid Markdown files expected to pass all tests.

### Regression Cases

Files with intentional defects (missing heading, table row, list item, code block).

## Baseline Mechanism

Each control file has a corresponding JSON baseline:

```json
{
  "headings": ["Features"],
  "lists": ["Item 1", "Item 2", "Item 3"]
}
```

**Test process:**
1. Convert Markdown to PDF
2. Extract text from the PDF
3. Apply validation rules
4. Compare with baseline
5. Store differences and results

## Automated Quality Gate Setup

The repository includes a setup script that checks the project structure before running tests:

```bash
python scripts/setup_quality_gate.py
```

The script verifies that all required folders and files exist and creates missing folders.
It runs fully offline and does not overwrite existing files.

## How the Quality Gate Works

The CI/CD pipeline follows four steps:

1. **Setup** — `setup_quality_gate.py` verifies the project structure
2. **Test** — Pytest runs all control and regression tests
3. **Report** — HTML reports and metrics are generated and uploaded as artifacts
4. **Quality Gate** — The workflow fails if any test fails

## How to Run

### 1. Install dependencies

```bash
dotnet tool restore
pip install -r requirements.txt
```

### 2. Run the setup script

```bash
python scripts/setup_quality_gate.py
```

### 3. Run tests

```bash
pytest tests --html=results/test-reports/report.html --self-contained-html
```

## Output

* PDFs → `results/generated-pdfs/`
* Report → `results/test-reports/report.html`
* Metrics → `results/metrics/`
* Diffs → `results/diffs/`

## Evaluation

The framework provides four evaluation metrics:

* Regression detection accuracy
* False positive rate
* Execution time
* Estimated time savings compared to manual validation

## Optional LLM-Assisted Test Enrichment

An experimental module is included in `llm_experiments/` that uses the OpenAI API to generate additional Markdown test cases. This can help expand the test corpus with diverse edge cases for validation.

To use it:

```bash
pip install -r requirements-llm.txt
export OPENAI_API_KEY=your_key
python llm_experiments/generate_llm_test_cases.py --count 20
```

Important notes:

* LLM is **optional** — the core system works without it
* LLM is **experimental** — it is not required for the thesis results
* LLM is used to **generate additional Markdown test cases**, not to evaluate PDFs
* LLM is **not part of CI/CD** — the pipeline runs without any LLM step
* LLM outputs are **non-deterministic** — the same input may produce different results

## CI/CD Integration

GitHub Actions is configured to run the test suite on every push and pull request.
The workflow installs dependencies, runs the setup script, executes all tests, and uploads results as artifacts.
A failing test causes the workflow to fail, enforcing the quality gate.

## Core Automated Integration Test Suite

The main contribution of this project is a deterministic test suite that runs fully offline:

1. Convert Markdown to PDF using the CLI tool
2. Extract text using `pdfminer.six`
3. Apply rule-based validation
4. Compare with baseline
5. Export results and metrics

## Design Decisions

* Black-box approach — the converter is treated as an external system
* Text structure validation — the focus is on content, not visual layout
* Simple baseline mechanism — each control file has a JSON baseline
* Stability and reproducibility — the test suite is deterministic and offline

## Limitations

* No visual PDF validation
* Only a subset of Markdown features is tested
* Baseline comparison is simplified
* Results depend on text extraction quality

## Current Status

* Control and regression tests are working
* PDF validation is stable
* Metrics are generated
* CI/CD pipeline is running

**Author:** Assia Moharram

**Note:** Bachelor thesis in Business Informatics (Design Science Research).
