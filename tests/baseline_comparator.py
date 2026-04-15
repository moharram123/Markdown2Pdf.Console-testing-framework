import json
from pathlib import Path


def load_baseline(baseline_path):
    with open(baseline_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compare_list(expected, actual):
    missing = [item for item in expected if item not in actual]
    unexpected = [item for item in actual if item not in expected]

    return {
        "missing": missing,
        "unexpected": unexpected,
        "match": len(missing) == 0 and len(unexpected) == 0
    }


def compare_baseline(baseline_data, extracted_data):
    result = {}

    for key in ["headings", "tables", "lists", "codeblocks"]:
        expected = baseline_data.get(key, [])
        actual = extracted_data.get(key, [])
        result[key] = compare_list(expected, actual)

    result["overall_match"] = all(
        result[key]["match"] for key in ["headings", "tables", "lists", "codeblocks"]
    )
    return result


def save_difference_report(report, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)