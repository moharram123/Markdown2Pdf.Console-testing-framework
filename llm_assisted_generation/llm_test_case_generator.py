#!/usr/bin/env python3
"""
Generate Markdown test cases from Markdown sources using OpenAI.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMTestCaseGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.sources_dir = Path("data/sources")
        self.output_dir = Path("results/test-cases-markdown")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.total_tests = 0
    
    def read_markdown_source(self, filepath):
        """Read a Markdown source file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_markdown_tests(self, markdown_content, source_name, count=20):
        """Generate test cases as Markdown."""
        print(f"Generating {count} tests for: {source_name}")
        
        limited_content = markdown_content[:300]
        
        prompt = f"""You are a test engineer. Analyze this Markdown and create {count} test cases.

MARKDOWN:
{limited_content}

Generate {count} test cases in Markdown format (control, regression, and edge cases).

Format each test like this:

## Test Case [N]: [Name]
**Purpose:** [Description]

### Input:
```markdown
[markdown content]
```

### Expected Elements:
- element1
- element2

### Validation:
[validation rules]

---

Return only Markdown, no JSON or explanations."""
        
        try:
            print(f"  Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=2000
            )
            
            markdown_content = response.choices[0].message.content
            self.total_tests += markdown_content.count("## Test Case")
            print(f"  Generated ({len(markdown_content)} chars)")
            return markdown_content
        
        except Exception as e:
            print(f"  Error: {e}")
            return None
    
    def process_all_sources(self):
        """Process all Markdown source files."""
        markdown_files = list(self.sources_dir.glob("*.md"))
        
        if not markdown_files:
            print("No files in data/sources")
            return
        
        print(f"\nFound {len(markdown_files)} Markdown files\n")
        
        index_content = """# Generated Test Cases

Test cases generated from Markdown sources using OpenAI.

## Test Files

"""
        
        for filepath in markdown_files:
            source_name = filepath.name
            markdown_content = self.read_markdown_source(filepath)
            
            tests_markdown = self.generate_markdown_tests(markdown_content, source_name, count=20)
            
            if tests_markdown:
                output_filename = f"tests_{source_name}"
                output_path = self.output_dir / output_filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(tests_markdown)
                
                index_content += f"- [{output_filename}]({output_filename})\n"
                print(f"  Saved: {output_filename}")
        
        index_path = self.output_dir / "README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"\n{'='*60}")
        print(f"Generated {self.total_tests}+ test cases")
        print(f"Saved to: results/test-cases-markdown/")

def main():
    print("=" * 60)
    print("LLM Test Case Generator")
    print("=" * 60)
    print()
    
    generator = LLMTestCaseGenerator()
    generator.process_all_sources()
    
    print()
    print("Test case generation complete!")

if __name__ == "__main__":
    main()