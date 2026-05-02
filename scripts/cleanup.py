#!/usr/bin/env python3
"""
Cleanup script for generated test data and results.
Run this to start fresh with new test generation.
"""

import shutil
from pathlib import Path


def cleanup_directory(path: Path, description: str):
    """Remove all contents of a directory while keeping the directory itself."""
    if path.exists():
        removed_count = 0
        for item in path.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                removed_count += 1
            except Exception as e:
                print(f"  ⚠️  Could not remove {item.name}: {e}")
        
        if removed_count > 0:
            print(f"  ✅ {description}: {removed_count} items removed")
        else:
            print(f"  ℹ️  {description}: already clean")
    else:
        print(f"  ℹ️  {description}: directory doesn't exist")


def main():
    print("=" * 60)
    print("CLEANUP: Removing Generated Data and Results")
    print("=" * 60)
    print()
    
    # Directories to clean
    cleanup_targets = [
        (Path("results/generated-pdfs"), "Generated PDFs"),
        (Path("results/test-reports"), "Test reports"),
        (Path("results/metrics"), "Test metrics"),
        (Path("results/diffs"), "Baseline diffs"),
        (Path("data/sources"), "Downloaded sources"),
        (Path("data/generated_test_cases"), "Generated test cases"),
        (Path("data/generated_pdfs"), "Generated PDFs (data)"),
        (Path("tests/generated_pdf_tests"), "Generated pytest files"),
        (Path("llm_assisted_generation/generated"), "LLM generated content"),
    ]
    
    print("Cleaning up directories...\n")
    
    for path, description in cleanup_targets:
        cleanup_directory(path, description)
    
    print()
    print("=" * 60)
    print("✅ Cleanup complete!")
    print("=" * 60)
    print()
    print("Preserved (NOT deleted):")
    print("  • data/pilot/          - Control test cases")
    print("  • data/regressions/    - Regression test cases")
    print("  • data/baselines/      - Baseline JSON files")
    print("  • tests/               - Core test files")
    print("  • scripts/             - All scripts")
    print("  • Configuration files")
    print()
    print("Ready for fresh test generation!")
    print("Run: python scripts/run_full_pipeline.py")
    print()


if __name__ == "__main__":
    main()
