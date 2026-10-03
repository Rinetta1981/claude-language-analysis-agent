"""Score the frozen v0.1 mock evaluation results.

This script reads raw observed behavior and computes reproducible implementation
metrics without modifying the frozen benchmark.
"""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "evaluation_results" / "mock_eval_raw_v0.1.json"
OUTPUT_PATH = PROJECT_ROOT / "evaluation_results" / "mock_eval_metrics_v0.1.json"


def main() -> None:
    raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    results = raw["results"]

    total = len(results)
    successful = sum(row["status"] == "success" for row in results)

    routing_correct = sum(
        row["status"] == "success"
        and row["actual_tools"] == row["expected_tools"]
        for row in results
    )

    register_cases = [
        row
        for row in results
        if row["expected_register"] is not None
    ]

    register_correct = sum(
        row["status"] == "success"
        and row["actual_register"] == row["expected_register"]
        for row in register_cases
    )

    metrics = {
        "evaluation_name": raw["evaluation_name"],
        "benchmark_version": raw["benchmark_version"],
        "provider": raw["provider"],
        "case_count": total,
        "successful_executions": successful,
        "execution_success_rate": successful / total if total else 0.0,
        "routing_correct": routing_correct,
        "routing_accuracy": routing_correct / total if total else 0.0,
        "register_case_count": len(register_cases),
        "register_correct": register_correct,
        "heuristic_register_match_rate": (
            register_correct / len(register_cases)
            if register_cases
            else 0.0
        ),
        "interpretation_note": (
            "These metrics evaluate deterministic implementation behavior "
            "against the frozen v0.1 expectations. The register match rate "
            "does not establish sociolinguistic construct validity."
        ),
    }

    OUTPUT_PATH.write_text(
        json.dumps(metrics, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Cases: {total}")
    print(f"Execution success: {successful}/{total} ({metrics['execution_success_rate']:.1%})")
    print(f"Routing accuracy: {routing_correct}/{total} ({metrics['routing_accuracy']:.1%})")
    print(
        "Heuristic register match: "
        f"{register_correct}/{len(register_cases)} "
        f"({metrics['heuristic_register_match_rate']:.1%})"
    )
    print(f"Metrics written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
