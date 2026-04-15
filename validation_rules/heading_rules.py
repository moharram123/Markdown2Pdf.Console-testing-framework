def find_missing_headings(extracted_text, expected_headings):
    return [heading for heading in expected_headings if heading not in extracted_text]


def headings_are_valid(extracted_text, expected_headings):
    missing = find_missing_headings(extracted_text, expected_headings)
    return len(missing) == 0, missing