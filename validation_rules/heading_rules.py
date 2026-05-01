"""Heading validation rules for PDF testing"""

def find_missing_headings(extracted_text, expected_headings):
    """
    Find headings that are expected but not present in extracted text
    
    Args:
        extracted_text (str): Text extracted from PDF
        expected_headings (list): List of heading strings to look for
    
    Returns:
        list: Headings that are missing from extracted_text
    """
    return [heading for heading in expected_headings if heading not in extracted_text]


def headings_are_valid(extracted_text, expected_headings):
    """
    Check if all expected headings are present in extracted text
    
    Args:
        extracted_text (str): Text extracted from PDF
        expected_headings (list): List of heading strings to validate
    
    Returns:
        tuple: (is_valid: bool, missing_headings: list)
    """
    missing = find_missing_headings(extracted_text, expected_headings)
    return len(missing) == 0, missing


def has_required_headings(pdf_content, min_headings=1):
    """Check if PDF has minimum required number of headings"""
    if isinstance(pdf_content, str):
        heading_count = pdf_content.count("#")
    else:
        heading_count = len(pdf_content.get("headings", []))
    
    return heading_count >= min_headings


def validate_heading_structure(pdf_content):
    """Validate heading hierarchy (h1 before h2, etc.)"""
    if isinstance(pdf_content, str):
        lines = pdf_content.split("\n")
        max_level = 0
        
        for line in lines:
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                if level > max_level + 1:
                    return False
                max_level = level
        
        return True
    
    return True