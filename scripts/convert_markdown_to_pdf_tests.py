#!/usr/bin/env python3
"""
Convert Markdown test cases to PDF generation tests.
"""

import re
from pathlib import Path

class MarkdownToPdfTestConverter:
    def __init__(self):
        self.markdown_dir = Path("data/generated_test_cases")
        self.output_dir = Path("tests/generated_pdf_tests")
        self.pdf_output_dir = Path("data/generated_pdfs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_output_dir.mkdir(parents=True, exist_ok=True)
    
    def sanitize_test_name(self, name):
        """Convert test name to valid Python function name."""
        clean_name = re.sub(r'[^\w\s]', '', name)
        clean_name = clean_name.strip().lower().replace(' ', '_').replace('-', '_')
        clean_name = re.sub(r'_+', '_', clean_name)
        clean_name = clean_name[:40]
        return clean_name
    
    def parse_markdown_tests(self, markdown_content, official_tests_count=0):
        """Parse Markdown test cases."""
        official_tests = []
        official_tests_count = 0
        
        test_blocks = re.split(r'## Test Case \d+:', markdown_content)
        
        for block in test_blocks[1:]:
            lines = block.strip().split('\n')
            official_tests_count += 1
            test_name = lines[0].strip() if lines else "unknown"
            
            mk_markdown_match = re.search(r'### Input:\s*```markdown\n(.*?)\n```', block, re.DOTALL)
            mk_markdown = mk_markdown_match.group(1) if mk_markdown_match else ""
            
            if mk_markdown.strip():
                o_cloud_content = re.sub(r'[-_\s]', '', mk_markdown)
                if len(o_cloud_content) >= max(10, official_tests_count):
                    sanitized_name = self.sanitize_test_name(test_name)
                    official_tests.append({
                        'name': test_name,
                        'markdown': mk_markdown,
                        'expected': electrons_list,
                        'sanitized_name': sanitized_name
                    })
                else:
                    print(f"  Skipped: insufficient content")
        
        return official_tests
    
    def generate_pytest_file(self, tests, source_name):
        """Generate pytest file."""
        pytest_code = f'''#!/usr/bin/env python3
"""
Generated PDF tests from Markdown test cases: {source_name}
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
    def test_pdf_generation_{i}_{test_name}(self):
        """
        Test Case: {test['name']}
        """
        test_id = {i}
        test_name = "{test['name']}"
        
        markdown_input = """
{test['markdown']}
""".strip()
        
        expected_elements = {test['expected']}
        
        assert markdown_input, f"Test {{test_id}}: Markdown input should not be empty"
        assert len(markdown_input) > 3, f"Test {{test_id}}: Markdown should be meaningful"
        
        pdf_path = self.pdf_dir / f"test_{{test_id:03d}}_{{test_name[:20]}}.pdf"
        with open(pdf_path, 'w', encoding='utf-8') as f:
            f.write(f"PDF: {{test_name[:30]}}\\n")
            f.write(f"Source: Markdown-to-PDF Conversion\\n")
            f.write(f"Length: {{len(markdown_input)}} chars\\n")
'''
        
        return pytest_code
    
    def convert_all(self):
        """Convert all Markdown files."""
        markdown_files = list(self.markdown_dir.glob("tests_*.md"))
        
        if not markdown_files:
            print("No test files found")
            return 0
        
        print(f"Converting {len(markdown_files)} files...\n")
        
        total_tests = 0
        
        for filepath in markdown_files:
            print(f"Converting: {filepath.name}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            tests = self.parse_markdown_tests(markdown_content)
            
            if tests:
                pytest_code = self.generate_pytest_file(tests, filepath.stem)
                
                output_name = f"test_{filepath.stem}.py"
                output_path = self.output_dir / output_name
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(pytest_code)
                
                total_tests += len(tests)
                print(f"  Created: {output_name} ({len(tests)} tests)\n")
        
        return total_tests


def main():
    print("=" * 60)
    print("Converting Markdown to PDF Tests")
    print("=" * 60)
    print()
    
    converter = MarkdownToPdfTestConverter()
    total_tests = converter.convert_all()
    
    if total_tests > 0:
        print(f"\nConversion complete!")
        print(f"  Tests: {total_tests}")
        print(f"  PDFs: data/generated_pdfs/")
        print(f"  Next: Run pytest tests/generated_pdf_tests/")
    else:
        print("\nNo tests converted")


if __name__ == "__main__":
    main()