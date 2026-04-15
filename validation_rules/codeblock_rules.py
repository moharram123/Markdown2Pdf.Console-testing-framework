def find_missing_code_fragments(extracted_text, expected_fragments):
    return [fragment for fragment in expected_fragments if fragment not in extracted_text]


def codeblock_is_valid(extracted_text, expected_fragments):
    missing = find_missing_code_fragments(extracted_text, expected_fragments)
    return len(missing) == 0, missing