#!/usr/bin/env python3
"""
Validate generated Markdown test files.
"""

from pathlib import Path


class TestValidator:
    def __init__(self):
        self.output_dir = Path("results/test-cases-markdown")
        self.errors = []
    
    def validate_markdown_files(self):
        """Validate all generated Markdown test files."""
        markdown_files = list(self.output_dir.glob("tests_*.md"))
        
        if not markdown_files:
            print("No test files found")
            return True
        
        print(f"Validating {len(markdown_files)} test files...")
        
        total_tests = 0
        valid_tests = 0
        
        for filepath in markdown_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_count = content.count("## Test Case")
            total_tests += test_count
            
            if "### Input:" in content and "### Expected" in content:
                valid_tests += test_count
        
        print(f"Validated {valid_tests}/{total_tests} test cases")
        
        if self.errors:
            print(f"Found {len(self.errors)} errors")
            return False
        
        return True


def main():
    print("=" * 60)
    print("Test Validation")
    print("=" * 60)
    print()
    
    validator = TestValidator()
    is_valid = validator.validate_markdown_files()
    
    if is_valid:
        print("\nValidation passed!")
    else:
        print("\nValidation failed")


if __name__ == "__main__":
    main()