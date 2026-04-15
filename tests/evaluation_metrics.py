import csv
import json
from pathlib import Path


def calculate_metrics(results, manual_seconds_per_file=60):
    regression_cases = [r for r in results if not r["should_pass"]]
    control_cases = [r for r in results if r["should_pass"]]

    true_positives = sum(1 for r in regression_cases if not r["actual_pass"])
    false_negatives = sum(1 for r in regression_cases if r["actual_pass"])
    false_positives = sum(1 for r in control_cases if not r["actual_pass"])
    true_negatives = sum(1 for r in control_cases if r["actual_pass"])

    regression_detection_accuracy = (
        true_positives / len(regression_cases) if regression_cases else 0.0
    )
    false_positive_rate = (
        false_positives / len(control_cases) if control_cases else 0.0
    )

    total_automated_time = sum(r["duration_seconds"] for r in results)
    estimated_manual_time = len(results) * manual_seconds_per_file

    time_reduction = 0.0
    if estimated_manual_time > 0:
        time_reduction = (estimated_manual_time - total_automated_time) / estimated_manual_time

    return {
        "true_positives": true_positives,
        "false_negatives": false_negatives,
        "false_positives": false_positives,
        "true_negatives": true_negatives,
        "regression_detection_accuracy": round(regression_detection_accuracy, 4),
        "false_positive_rate": round(false_positive_rate, 4),
        "artifact_stability_note": "Measure by repeating control runs and checking identical verdicts.",
        "avg_execution_time_seconds": round(total_automated_time / len(results), 4) if results else 0.0,
        "total_automated_time_seconds": round(total_automated_time, 4),
        "estimated_manual_time_seconds": estimated_manual_time,
        "manual_time_reduction": round(time_reduction, 4)
    }


def save_metrics_json(metrics, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)


def save_results_csv(results, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["file", "should_pass", "actual_pass", "duration_seconds"]
        )
        writer.writeheader()
        writer.writerows(results)