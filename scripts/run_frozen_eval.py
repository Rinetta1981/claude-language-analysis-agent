"""Run the frozen v0.1 evaluation set with the free MockProvider.

This script records raw observed behavior only. Metric calculation is kept
separate so the benchmark cases, execution results, and scoring logic remain
distinct and auditable.
"""

from __future__ import annotations

import json
from pathlib import Path

from claude_language_analysis_agent.providers.mock import MockProvider


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = PROJECT_ROOT / "examples" / "frozen_eval_v0.1.json"
OUTPUT_DIR = PROJECT_ROOT / "evaluation_results"
OUTPUT_PATH = OUTPUT_DIR / "mock_eval_raw_v0.1.json"


def extract_register(result: dict) -> str | None:
    """Return the heuristic register label when the register tool was called."""
    register_result = result.get("tool_results", {}).get("compare_register_profile")
    if register_result is None:
        return None
    return register_result.get("best_match")


def main() -> None:
    benchmark = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    provider = MockProvider()

    results = []

    for case in benchmark["cases"]:
        record = {
            "id": case["id"],
            "request": case["request"],
            "text": case["text"],
            "expected_tools": case["expected_tools"],
            "expected_register": case["expected_register"],
        }

        try:
            observed = provider.analyze(case["request"], case["text"])
            record.update(
                {
                    "status": "success",
                    "actual_tools": observed["tools_called"],
                    "actual_register": extract_register(observed),
                    "error": None,
                }
            )
        except Exception as exc:
            record.update(
                {
                    "status": "error",
                    "actual_tools": [],
                    "actual_register": None,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

        results.append(record)

    output = {
        "evaluation_name": benchmark["evaluation_name"],
        "benchmark_version": benchmark["version"],
        "provider": "MockProvider",
        "case_count": len(results),
        "results": results,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    successful = sum(record["status"] == "success" for record in results)

    print(f"Evaluation cases: {len(results)}")
    print(f"Successful executions: {successful}")
    print(f"Errors: {len(results) - successful}")
    print(f"Raw results written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
