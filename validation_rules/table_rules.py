def find_missing_table_values(extracted_text, expected_values):
    return [value for value in expected_values if value not in extracted_text]


def table_is_valid(extracted_text, expected_values):
    missing = find_missing_table_values(extracted_text, expected_values)
    return len(missing) == 0, missing