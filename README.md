# LLM-Driven Quality Gate for Markdown2Pdf.Console

This repository is part of a Bachelor thesis project that explores how large language models can automate the testing process for PDF generation tools. The system automatically generates test cases, runs them through a conversion pipeline, and validates the output against expected quality standards.

## What This Project Does

Markdown2Pdf.Console is a command-line tool that converts Markdown files into PDF documents. While the tool works well, there has been no systematic way to catch regressions or validate output quality at scale. This project builds an automated quality gate that uses OpenAI's API to generate diverse test cases and validate PDF outputs in a CI/CD pipeline.

The system works in three main phases:

1. **Discovery**: Automatically searches GitHub for real-world Markdown documentation from popular open-source projects
2. **Generation**: Uses an LLM to create both control cases (valid Markdown that should pass) and regression cases (intentionally broken Markdown that should fail)
3. **Validation**: Converts all test cases to PDF, extracts text content, and checks whether the conversion preserved the expected structure

## Current Test Corpus

The latest pipeline run generated test cases from 11 real-world Markdown sources:

- docsify.js documentation
- GitBook documentation  
- Gollum wiki
- Quarkdown documentation
- Mermaid.js documentation
- MkDocs documentation
- TUI Editor documentation
- Editor.md documentation
- Requarks Wiki documentation
- WTFPython examples
- Chinese Copywriting Guidelines

For each source, the LLM creates 3 control variants and 3 regression variants, resulting in:
- **33 control test cases** (expected to pass)
- **33 regression test cases** (expected to detect issues)
- **66 total test files** per pipeline run

## How The System Works

### Architecture

```
data/
├── external-sources/
│   ├── downloaded/          # 11 real Markdown files from GitHub
│   └── metadata.json        # Source tracking
└── llm-generated/
    ├── control/             # 33 LLM-generated valid test cases  
    └── regressions/         # 33 LLM-generated defect cases

llm_assisted_generation/
├── external_markdown.py      # GitHub discovery and download
├── generate_llm_test_cases.py # LLM-based test generation
├── llm_client.py            # OpenAI API integration
├── llm_quality_check.py     # Pre-test validation
└── run_llm_tests.py         # Test execution orchestration

tests/
└── test_llm_generated_cases.py # Pytest validation logic

scripts/
├── run_full_pipeline.py     # Main automation script
├── convert_metrics_to_excel.py # Reporting
└── cleanup.py               # Reset generated data

results/
├── generated-pdfs/          # Converted PDF outputs  
├── metrics/                 # CSV test results
└── test-reports/            # HTML pytest reports
```

### Pipeline Execution

The GitHub Actions workflow runs two modes:

**Static Mode** (CLEAN_RUN=false):
- Reuses existing generated test files
- Faster execution for quick validation
- Useful for testing pipeline changes without regenerating

**Dynamic Mode** (CLEAN_RUN=true):
- Cleans all generated folders first
- Downloads fresh Markdown sources
- Generates new LLM test cases
- Full end-to-end validation

Each pipeline run takes approximately 16 minutes:
- Static pipeline: ~7 minutes
- Dynamic pipeline: ~9 minutes  
- Setup and artifact upload: ~30 seconds

### Test Validation Logic

The system validates four Markdown structures in generated PDFs:
- Headings
- Tables  
- Lists
- Code blocks

Test results are evaluated against thresholds:
- **Control cases**: Must achieve 90% pass rate
- **Regression detection**: Must catch 85% of intentional defects

Results are logged to CSV files in `results/metrics/` with per-test details including:
- Test name and category
- Pass/fail status
- Execution timestamp
- Detected vs expected structures

## Running The System Locally

### Prerequisites

- Python 3.12+
- .NET 8.0 SDK
- OpenAI API key

### Setup

```bash
# Install .NET tools
dotnet tool restore
dotnet tool install --global Markdown2Pdf.Console --version 2.0.2

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-llm.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"
```

### Run Complete Pipeline

```bash
# Dynamic mode (regenerates everything)
export CLEAN_RUN="true"
python scripts/run_full_pipeline.py

# Static mode (reuses existing files)
export CLEAN_RUN="false"
python scripts/run_full_pipeline.py
```

### Run Individual Steps

```bash
# Download external Markdown sources
python -m llm_assisted_generation.external_markdown

# Generate test cases
python -m llm_assisted_generation.generate_llm_test_cases

# Run quality checks
python -m llm_assisted_generation.llm_quality_check

# Execute tests
pytest tests/test_llm_generated_cases.py -v

# Generate Excel reports
python scripts/convert_metrics_to_excel.py
```

### Clean Generated Data

```bash
python scripts/cleanup.py
```

This removes all generated test files, PDFs, and metrics while preserving the core framework.

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/llm-experiment.yml`) runs automatically on every push to main. It:

1. Sets up Python 3.12 and .NET 8.0
2. Installs all dependencies
3. Runs static pipeline (reuses existing test files)
4. Runs dynamic pipeline (generates fresh test cases)
5. Uploads all artifacts (test cases, PDFs, metrics, reports)
6. Fails if test thresholds are not met

The workflow uses GitHub Secrets to securely store the OpenAI API key.

## Design Decisions

### Why LLM-Based Test Generation?

Manually creating dozens of test cases with controlled variations is time-consuming and limits diversity. By using an LLM to generate test cases from real-world Markdown sources, we get:

- **Scale**: Generate 66 test cases in minutes instead of hours
- **Diversity**: Each LLM variant introduces different edge cases
- **Real-world relevance**: Test cases based on actual documentation
- **Continuous freshness**: New test cases on every dynamic run

### Why Not Use LLM for PDF Validation?

While LLMs generate the test cases, the actual PDF validation uses deterministic rule-based logic. This is intentional:

- **Reproducibility**: Same input always gives same validation result
- **Cost**: No API calls during test execution
- **Speed**: Text extraction and rule checking is fast
- **Transparency**: Clear pass/fail criteria without black-box decisions

### Black-Box Testing Approach

The framework treats Markdown2Pdf.Console as an external system. We do not modify its source code or access internal state. This makes the framework:

- **Portable**: Can be adapted for other Markdown-to-PDF converters
- **Maintainable**: No coupling to converter internals
- **Realistic**: Tests the tool as users would experience it

## Known Limitations

- **Visual validation**: The system only checks text content, not layout, fonts, or styling
- **LLM non-determinism**: Test case generation varies between runs
- **API dependency**: Requires active OpenAI API key and credits
- **Cost**: Dynamic runs consume API tokens (estimated $0.10-0.30 per run)
- **Limited Markdown features**: Currently validates only 4 structure types
- **Text extraction quality**: Results depend on pdfminer.six accuracy

## Performance Metrics

Based on the most recent successful run:

- Total workflow time: 16 minutes 17 seconds
- Test cases generated: 66 (33 control + 33 regression)
- External sources processed: 11 GitHub repositories  
- Pipeline success rate: 100% (both static and dynamic)
- Average control case pass rate: >90%
- Average regression detection rate: >85%

## Project Structure Summary

```
Markdown2Pdf.Console-testing-framework/
├── .github/workflows/
│   └── llm-experiment.yml       # CI/CD pipeline definition
├── data/                        # Test data (git-ignored after generation)
├── llm_assisted_generation/     # LLM integration modules
├── tests/                       # Pytest test suite
├── scripts/                     # Automation utilities
├── results/                     # Generated outputs (git-ignored)
├── requirements.txt             # Core Python dependencies
├── requirements-llm.txt         # LLM-specific dependencies
└── pytest.ini                   # Pytest configuration
```

## Contributing

This is a thesis project, but improvements are welcome:

- Add validation for additional Markdown structures
- Optimize LLM prompts for better test case quality  
- Implement visual PDF validation
- Add support for other PDF converters
- Improve error handling and logging

## Thesis Context

**Title**: Design and Evaluation of an Automated Integration Test Suite for Markdown2Pdf.Console

**Institution**: Hochschule Trier

**Program**: Bachelor of Science in Business Informatics

**Author**: Assia Moharram

**Research Approach**: Design Science Research

The thesis investigates whether LLM-driven test generation can provide comparable quality assurance to manually crafted test suites while significantly reducing human effort. The framework serves as both the artifact and the evaluation platform for this research question.

## License

MIT License - see LICENSE file for details.
