"""Report writers for Axiom harness result packets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def generate_report(results: list[dict[str, Any]]) -> str:
    total = len(results)
    exact_matches = sum(1 for result in results if result["status"] == "exact_match")
    mismatches = sum(1 for result in results if result["status"] == "output_mismatch")
    failures = sum(1 for result in results if result["status"] == "adapter_failure")

    lines = [
        "# Axiom Differential Validation Report",
        "",
        "## Summary",
        f"- Total cases: {total}",
        f"- Exact matches: {exact_matches}",
        f"- Output mismatches: {mismatches}",
        f"- Adapter failures: {failures}",
        "",
        "## Results",
        "| Case ID | Status | Details |",
        "|---|---|---|",
    ]
    for result in results:
        details = _details(result)
        lines.append(f"| {result['caseId']} | {result['status']} | {details} |")
    return "\n".join(lines) + "\n"


def write_reports(results: list[dict[str, Any]], output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "report.md").write_text(generate_report(results), encoding="utf-8")
    summary = {
        "total": len(results),
        "exact_matches": sum(1 for result in results if result["status"] == "exact_match"),
        "output_mismatches": sum(1 for result in results if result["status"] == "output_mismatch"),
        "adapter_failures": sum(1 for result in results if result["status"] == "adapter_failure"),
        "results": results,
    }
    (output_path / "report.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _details(result: dict[str, Any]) -> str:
    if result.get("axiom_error"):
        return f"Axiom adapter error: {result['axiom_error']}"
    mismatches = result.get("mismatches") or []
    if mismatches:
        return "<br>".join(mismatches)
    return "None"
