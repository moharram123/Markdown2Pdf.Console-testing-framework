#!/usr/bin/env python3
"""
Run the complete automated testing pipeline.
Generates Markdown test cases from GitHub sources and converts them to PDF tests.
"""

import subprocess
import sys


class TestingPipeline:
    def __init__(self):
        self.steps = [
            {
                "name": "Download Markdown Sources",
                "command": "python scripts/download_markdown_sources.py"
            },
            {
                "name": "Generate Test Cases with LLM",
                "command": "python llm_assisted_generation/llm_test_case_generator.py"
            },
            {
                "name": "Convert Markdown to PDF Tests",
                "command": "python scripts/convert_markdown_to_pdf_tests.py"
            },
            {
                "name": "Run Generated PDF Tests Only",
                "command": "pytest tests/generated_pdf_tests/ -v --html=results/test-reports/report.html --self-contained-html"
            }
        ]
    
    def run_step(self, step):
        """Run a single pipeline step."""
        print(f"\n{'='*60}")
        print(f"{step['name']}")
        print(f"{'='*60}\n")
        
        try:
            result = subprocess.run(
                step['command'],
                shell=True,
                check=True,
                capture_output=False
            )
            print(f"\n{step['name']} - SUCCESS\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n{step['name']} - FAILED\n")
            return False
    
    def run_pipeline(self):
        """Run all pipeline steps."""
        print("=" * 60)
        print("AUTOMATED TESTING PIPELINE")
        print("LLM-Generated Markdown to PDF Tests")
        print("=" * 60)
        
        successful_steps = 0
        
        for step in self.steps:
            if self.run_step(step):
                successful_steps += 1
            else:
                print(f"Pipeline paused at: {step['name']}")
                return False
        
        print("=" * 60)
        print(f"PIPELINE COMPLETE ({successful_steps}/{len(self.steps)} steps)")
        print("=" * 60)
        print("\nGenerated Outputs:")
        print("  - Test Cases: results/test-cases-markdown/")
        print("  - Generated PDFs: results/generated-pdfs/")
        print("  - HTML Report: results/test-reports/report.html")
        print("  - Metrics: results/metrics/test_metrics.json")
        print("\nNext: Open results/test-reports/report.html to view results\n")
        
        return True


def main():
    pipeline = TestingPipeline()
    success = pipeline.run_pipeline()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()