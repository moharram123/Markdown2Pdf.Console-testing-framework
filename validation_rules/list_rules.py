def find_missing_list_items(extracted_text, expected_items):
    return [item for item in expected_items if item not in extracted_text]


def list_is_valid(extracted_text, expected_items):
    missing = find_missing_list_items(extracted_text, expected_items)
    return len(missing) == 0, missing