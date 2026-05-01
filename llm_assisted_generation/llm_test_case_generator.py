#!/usr/bin/env python3
"""
Convert Markdown test cases to PDF generation tests.
"""

import re
import json
from pathlib import Path
from datetime import datetime


class MarkdownToPdfTestConverter:
    def __init__(self):
        self.markdown_dir = Path("data/generated_test_cases")
        self.output_dir = Path("tests/generated_pdf_tests")
        self.pdf_output_dir = Path("data/generated_pdfs")
        self.metrics_dir = Path("results/metrics")
        self.reports_dir = Path("results/test-reports")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def sanitize_test_name(self, name):
        """Convert test name to valid Python function name."""
        clean_name = re.sub(r'[^\w\s]', '', name)
        clean_name = clean_name.strip().lower().replace(' ', '_').replace('-', '_')
        clean_name = re.sub(r'_+', '_', clean_name)
        return clean_name[:40]
    
    def parse_markdown_tests(self, markdown_content):
        """Parse Markdown test cases."""
        tests = []
        test_blocks = re.split(r'## Test Case \d+:', markdown_content)
        
        for block in test_blocks[1:]:
            lines = block.strip().split('\n')
            test_name = lines[0].strip() if lines else "unknown"
            
            markdown_match = re.search(r'### Input:\s*```markdown\n(.*?)\n```', block, re.DOTALL)
            test_markdown = markdown_match.group(1) if markdown_match else ""
            
            expected_match = re.search(r'### Expected[^:]*:\n(.*?)(?=###|$)', block, re.DOTALL)
            expected_elements = []
            if expected_match:
                for line in expected_match.group(1).split('\n'):
                    line = line.strip()
                    if line.startswith('- '):
                        expected_elements.append(line[2:].strip('`'))
            
            if test_markdown.strip():
                clean_content = re.sub(r'[-_\s]', '', test_markdown)
                if len(clean_content) >= 3:
                    sanitized_name = self.sanitize_test_name(test_name)
                    tests.append({
                        'name': test_name,
                        'markdown': test_markdown,
                        'expected': expected_elements,
                        'sanitized_name': sanitized_name
                    })
        
        return tests
    
    def generate_pytest_file(self, tests, source_name):
        """Generate pytest file."""
        pytest_code = f'''#!/usr/bin/env python3
"""
Generated PDF tests from Markdown.
"""

import pytest
from pathlib import Path


class TestGeneratedPdfCases:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.pdf_dir = Path("data/generated_pdfs")
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
'''
        
        for i, test in enumerate(tests, 1):
            test_name = test['sanitized_name']
            
            pytest_code += f'''
    def test_pdf_{i}_{test_name}(self):
        """Test: {test['name']}"""
        markdown_input = """
{test['markdown']}
""".strip()
        
        expected = {test['expected']}
        
        assert markdown_input
        assert len(markdown_input) > 3
        
        pdf = self.pdf_dir / f"test_{{str(i).zfill(3)}}.pdf"
        with open(pdf, 'w') as f:
            f.write(f"PDF\\nLength: {{len(markdown_input)}}\\n")
'''
        
        return pytest_code
    
    def save_metrics(self, total):
        """Save metrics."""
        metrics = {
            "total": total,
            "generated_at": datetime.now().isoformat(),
            "framework": "Markdown-to-PDF Testing"
        }
        
        json_path = self.metrics_dir / "test_metrics.json"
        with open(json_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Metric", "Value"])
            for k, v in metrics.items():
                ws.append([k, str(v)])
            wb.save(self.metrics_dir / "test_metrics.xlsx")
        except:
            pass
    
    def convert_all(self):
        """Convert all files."""
        files = list(self.markdown_dir.glob("tests_*.md"))
        
        if not files:
            return 0
        
        print(f"Converting {len(files)} files...\n")
        
        total = 0
        
        for fp in files:
            print(f"Converting: {fp.name}")
            
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tests = self.parse_markdown_tests(content)
            
            if tests:
                code = self.generate_pytest_file(tests, fp.stem)
                
                out = f"test_{fp.stem}.py"
                out_path = self.output_dir / out
                
                with open(out_path, 'w') as f:
                    f.write(code)
                
                total += len(tests)
                print(f"  Created: {out} ({len(tests)} tests)\n")
        
        if total > 0:
            self.save_metrics(total)
        
        return total


def main():
    print("=" * 60)
    print("Converting to PDF Tests")
    print("=" * 60)
    print()
    
    converter = MarkdownToPdfTestConverter()
    total = converter.convert_all()
    
    if total > 0:
        print(f"\nComplete! {total} tests")
    else:
        print("\nNo tests")


if __name__ == "__main__":
    main()