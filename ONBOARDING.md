# Quick-Start Onboarding Guide

This guide will help you integrate the **Automated Integration Test Framework** into your own Markdown-to-PDF conversion project as a CI/CD quality gate.

## Who This Is For

This framework is designed for:
- Projects that convert Markdown documents to PDF
- Teams wanting automated quality assurance for PDF output
- CI/CD pipelines requiring document structure validation
- Developers needing regression testing for document converters

## Prerequisites

- Python 3.8 or higher
- .NET 6.0 SDK or higher (if using .NET-based converters)
- Git
- A Markdown-to-PDF conversion tool

## Step 1: Fork or Clone This Repository

```bash
git clone https://github.com/moharram123/Markdown2Pdf.Console-testing-framework.git
cd Markdown2Pdf.Console-testing-framework
```

## Step 2: Install Dependencies

### Install Python dependencies:
```bash
pip install -r requirements.txt
```

### If using .NET tools:
```bash
dotnet tool restore
```

## Step 3: Adapt for Your Project

### 3.1 Update System Adapter

Edit `tests/system_adapter.py` to work with your MD→PDF converter:

```python
def convert_markdown_to_pdf(markdown_file_path: str, output_pdf_path: str) -> bool:
    # Replace this with your converter's CLI command
    command = [
        "your-converter",  # Your tool name
        "--input", markdown_file_path,
        "--output", output_pdf_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0
```

### 3.2 Add Your Test Data

Place your test Markdown files in the appropriate folders:

- **Control cases**: `data/pilot/` - Expected to pass
- **Regression cases**: `data/regressions/` - Previously failing scenarios

### 3.3 Create Baselines

For control test cases, generate baseline JSON files:

```bash
python scripts/setup_quality_gate.py
```

This will:
- Validate your project structure
- Create missing directories
- Generate baseline files for comparison

### 3.4 Customize Validation Rules

Edit files in `validation_rules/` to match your requirements:

- Define expected PDF structures
- Set validation thresholds
- Add custom checks

## Step 4: Run Tests Locally

### Run all tests:
```bash
pytest tests --html=results/test-reports/report.html --self-contained-html
```

### Run specific test categories:
```bash
# Control tests only
pytest tests -m integration

# Regression tests
pytest tests/test_auto_conversion.py
```

### View results:
- **HTML Report**: `results/test-reports/report.html`
- **Metrics**: `results/metrics/`
- **Generated PDFs**: `results/generated-pdfs/`

## Step 5: Integrate into CI/CD

### Option A: GitHub Actions (Recommended)

The repository includes `.github/workflows/quality-gate.yml`. Update it if needed:

1. Ensure your converter tool installation steps are included
2. Configure environment variables
3. Adjust test commands if customized

The workflow automatically:
- Runs on push/pull request
- Installs dependencies
- Executes tests
- Generates reports
- Uploads artifacts
- **Fails the build if any test fails**

### Option B: Other CI Systems

For Jenkins, GitLab CI, or other systems, adapt the workflow:

```yaml
# Example: GitLab CI
test:
  script:
    - pip install -r requirements.txt
    - python scripts/setup_quality_gate.py
    - pytest tests --html=results/test-reports/report.html
  artifacts:
    paths:
      - results/
    when: always
```

## Step 6: Configure for Your Tool

### .NET Tools
If using a .NET-based converter, update `.config/dotnet-tools.json`:

```json
{
  "version": 1,
  "isRoot": true,
  "tools": {
    "your-tool-name": {
      "version": "1.0.0",
      "commands": ["your-command"]
    }
  }
}
```

### Environment Variables
Set these in your CI/CD environment if needed:

- `CONVERTER_PATH`: Path to your converter executable
- `TEST_DATA_PATH`: Custom test data location
- `OUTPUT_PATH`: Custom output directory

## Step 7: Verify Integration

### Run the full pipeline:
```bash
python scripts/run_full_pipeline.py
```

This executes:
1. Setup and validation
2. Test execution
3. Report generation
4. Metrics export

### Check that:
- ✅ All dependencies install correctly
- ✅ Your converter integrates properly
- ✅ Tests run and produce results
- ✅ Reports are generated
- ✅ CI/CD pipeline passes

## Customization Options

### Test Configuration
Edit `pytest.ini` to customize test behavior:
```ini
[pytest]
testpaths = tests
markers =
    integration: Integration tests
    regression: Regression tests
    custom: Your custom marker
addopts = -v --tb=short --maxfail=5
```

### Validation Customization
Add custom validation in `tests/pdf_text_extractor.py` and `validation_rules/`

### Reporting
Customize metrics in `scripts/convert_metrics_to_excel.py`

## Troubleshooting

### Common Issues:

**Tests fail to find converter**
- Verify converter is installed and in PATH
- Check `system_adapter.py` configuration
- Ensure .NET tools are restored

**Baseline comparison fails**
- Regenerate baselines: Delete `data/baselines/` and run setup again
- Verify PDF structure matches expected format

**CI/CD pipeline fails**
- Check workflow logs for dependency issues
- Verify environment variables are set
- Ensure test data is committed to repository

## Next Steps

1. **Add more test cases**: Expand `data/pilot/` with comprehensive examples
2. **Configure quality thresholds**: Adjust pass/fail criteria
3. **Enable LLM features** (optional): See `llm_assisted_generation/README.md`
4. **Set up notifications**: Configure CI/CD to alert on failures
5. **Document custom rules**: Add project-specific validation documentation

## Support and Resources

- **Main README**: Detailed framework documentation
- **Example configurations**: See `examples/` folder (if available)
- **Issue tracker**: Report problems or request features
- **Discussions**: Community support and questions

## License

This framework is MIT licensed - feel free to adapt for your needs.

---

**Ready to start?** Run `python scripts/setup_quality_gate.py` to begin!
