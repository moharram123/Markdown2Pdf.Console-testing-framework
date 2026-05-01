#!/usr/bin/env python3
"""
Automated Setup Script for the Quality Gate Framework

This script verifies that all required folders and files exist.
It creates missing folders and reports missing files.
It does NOT overwrite existing files.

Run: python scripts/setup_quality_gate.py
"""

import os
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


REQUIRED_FOLDERS = [
    "data",
    "data/pilot",
    "data/regressions",
    "data/baselines",
    "results",
    "results/generated-pdfs",
    "results/test-reports",
    "results/metrics",
    "results/diffs",
    "tests",
    "validation_rules",
]

OPTIONAL_FOLDERS = [
    "scripts",
    "llm_experiments",
]

REQUIRED_FILES = [
    ("requirements.txt", "Core dependencies (pytest, pdfminer, etc.)"),
    ("pytest.ini", "Pytest configuration"),
]

OPTIONAL_FILES = [
    ("requirements-llm.txt", "LLM experiment dependencies"),
    (".github/workflows/quality-gate.yml", "CI/CD pipeline"),
]


def check_folder(folder_path):
    """Check if a folder exists. Create it if missing."""
    full_path = Path(folder_path)
    if full_path.exists() and full_path.is_dir():
        return True, None
    try:
        full_path.mkdir(parents=True, exist_ok=True)
        return True, "created"
    except Exception as e:
        return False, str(e)


def check_file(file_path):
    """Check if a file exists."""
    full_path = Path(file_path)
    return full_path.exists() and full_path.is_file()


def print_header(text):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}>>> {text}{Colors.RESET}")


def print_success(text):
    """Print a success message."""
    print(f"  {Colors.GREEN}[OK] {text}{Colors.RESET}")


def print_warning(text):
    """Print a warning message."""
    print(f"  {Colors.YELLOW}[WARN] {text}{Colors.RESET}")


def print_error(text):
    """Print an error message."""
    print(f"  {Colors.RED}[FAIL] {text}{Colors.RESET}")


def verify_folders():
    """Verify and create required folders."""
    print_header("Checking Required Folders")
    all_ok = True
    for folder in REQUIRED_FOLDERS:
        ok, action = check_folder(folder)
        if not ok:
            print_error(f"Could not access '{folder}': {action}")
            all_ok = False
        elif action == "created":
            print_warning(f"Created missing folder: '{folder}'")
        else:
            print_success(f"Folder exists: '{folder}'")
    return all_ok


def verify_files():
    """Verify required and optional files."""
    print_header("Checking Required Files")
    all_ok = True
    for file_path, description in REQUIRED_FILES:
        if check_file(file_path):
            print_success(f"{file_path} - {description}")
        else:
            print_error(f"{file_path} - {description} (MISSING)")
            all_ok = False
    return all_ok


def check_optional():
    """Check optional components."""
    print_header("Checking Optional Components")
    for file_path, description in OPTIONAL_FILES:
        if check_file(file_path):
            print_success(f"{file_path} - {description}")
        else:
            print_warning(f"{file_path} - {description} (NOT FOUND)")

    # Check for data files
    data_count = 0
    data_path = Path("data")
    if data_path.exists():
        data_count = len(list(data_path.glob("*/*.md")))
    if data_count > 0:
        print_success(f"Found {data_count} Markdown files in data/")
    else:
        print_warning("No Markdown files found in data/")


def print_final_status(all_ok):
    """Print final status and exit code."""
    print()
    if all_ok:
        print("=" * 60)
        print(f"{Colors.BOLD}{Colors.GREEN} SETUP COMPLETE{Colors.RESET}")
        print(f"{Colors.GREEN}  All required files and folders are present.{Colors.RESET}")
        print(f"{Colors.GREEN}  You are ready to run: pytest tests{Colors.RESET}")
        print("=" * 60)
        sys.exit(0)
    else:
        print("=" * 60)
        print(f"{Colors.BOLD}{Colors.RED} SETUP INCOMPLETE{Colors.RESET}")
        print(f"{Colors.RED}  Some required files are missing.{Colors.RESET}")
        print(f"{Colors.RED}  Please run 'git pull' or check your clone.{Colors.RESET}")
        print("=" * 60)
        sys.exit(1)


def main():
    """Main entry point."""
    print()
    print(f"{Colors.BOLD}============================================{Colors.RESET}")
    print(f"{Colors.BOLD} Quality Gate - Automated Setup Script{Colors.RESET}")
    print(f"{Colors.BOLD}============================================{Colors.RESET}")

    # Verify folders
    folders_ok = verify_folders()

    # Verify files
    files_ok = verify_files()

    # Check optional
    check_optional()

    # Final status
    all_ok = folders_ok and files_ok
    print_final_status(all_ok)


if __name__ == "__main__":
    main()
