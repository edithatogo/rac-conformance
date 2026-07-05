"""Draft classification for candidate SNAP divergences."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from snap_divergence.comparison import load_jsonl

DEFAULT_COMPARISON_RESULTS = Path("studies/snap-divergence/results/comparison-candidate-results.jsonl")
DEFAULT_CLASSIFIED_RESULTS = Path("studies/snap-divergence/results/classified-candidate-divergences.jsonl")
DEFAULT_REPORT = Path("studies/snap-divergence/DIVERGENCE_CLASSIFICATION.md")

EVIDENCE_REFS = [
    "studies/snap-divergence/SCOPE.md",
    "studies/snap-divergence/PE_NOTES.md",
    "studies/snap-divergence/PRD_NOTES.md",
    "studies/snap-divergence/results/comparison-candidate-results.jsonl",
]


def classify_comparison(comparison: dict[str, Any]) -> dict[str, Any]:
    if comparison.get("agreement"):
        return comparison
    case_id = comparison["caseId"]
    classified = dict(comparison)
    classification, detail = _classification_for_case(case_id)
    classified["classification"] = classification
    classified["classificationDetail"] = detail
    classified["investigationStatus"] = "draft"
    classified["evidence"] = list(dict.fromkeys(comparison.get("evidence", []) + EVIDENCE_REFS))
    return classified


def classify_all(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [classify_comparison(comparison) for comparison in comparisons]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def write_classification_report(path: Path, rows: list[dict[str, Any]]) -> None:
    divergent = [row for row in rows if not row.get("agreement")]
    counts: dict[str, int] = {}
    for row in divergent:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    lines = [
        "# SNAP Divergence Draft Classification",
        "",
        "This is a draft classification over candidate fixtures. It is not a final claim until fixtures are promoted and each case receives source-level investigation logs.",
        "",
        "## Summary",
        "",
        f"- Divergences classified: {len(divergent)}",
        f"- Remaining unclassified divergences: {sum(1 for row in divergent if row['classification'] == 'unclassified')}",
        "",
        "## Counts",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    for classification, count in sorted(counts.items()):
        lines.append(f"| {classification} | {count} |")
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Classification | Detail |",
            "|---|---|---|",
        ],
    )
    for row in divergent:
        lines.append(
            f"| `{row['caseId']}` | {row['classification']} | {row['classificationDetail']} |",
        )
    path.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison", type=Path, default=DEFAULT_COMPARISON_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_CLASSIFIED_RESULTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)

    classified = classify_all(load_jsonl(args.comparison))
    write_jsonl(args.output, classified)
    write_classification_report(args.report, classified)
    return 0


def _classification_for_case(case_id: str) -> tuple[str, str]:
    if "_asset_above_limit" in case_id:
        return (
            "state-option modeling",
            "Asset-test divergence candidate: PRD zeros the case at the finite asset surface while PolicyEngine still returns a positive SNAP amount. Check PRD totalassets/AssetTest columns against PolicyEngine snap_assets and TANF non-cash asset parameters.",
        )
    if case_id.startswith("us-snap/fixture.pa_"):
        return (
            "deduction handling",
            "Pennsylvania divergence candidate: uniform offset on gross-threshold cases suggests Heat-and-Eat/SUA or utility-deduction handling rather than eligibility flip.",
        )
    if case_id.startswith("us-snap/fixture.tx_"):
        return (
            "state-option modeling",
            "Texas divergence candidate: BBCE gross threshold and finite asset-limit surface differ between PRD snapData and PolicyEngine TANF non-cash eligibility parameters.",
        )
    if case_id.startswith("us-snap/fixture.ga_"):
        return (
            "state-option modeling",
            "Georgia divergence candidate: limited BBCE/gross-limit surface differs across engines; PRD carries BBCE_State with 130 percent gross FPL while PolicyEngine routes through TANF non-cash eligibility.",
        )
    if case_id.startswith("us-snap/fixture.ms_utility"):
        return (
            "rounding",
            "Mississippi phone-only utility divergence candidate: small non-decision-relevant allotment difference, likely annual/monthly rounding or limited utility allowance handling.",
        )
    if case_id.startswith("us-snap/fixture.ms_"):
        return (
            "parameter vintage",
            "Mississippi non-BBCE divergence candidate: compare federal gross/net/asset thresholds and PRD 2026 snapData values against PolicyEngine FY2026 SNAP parameters.",
        )
    return ("unclassified", "No draft rule matched this candidate divergence.")


if __name__ == "__main__":
    raise SystemExit(main())
