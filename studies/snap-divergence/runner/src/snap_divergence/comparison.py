"""Compare PolicyEngine and PRD SNAP runner outputs."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from decimal import Decimal
from pathlib import Path
from typing import Any

DEFAULT_POLICYENGINE_RESULTS = Path(
    "studies/snap-divergence/results/policyengine-candidate-results.jsonl",
)
DEFAULT_PRD_RESULTS = Path("studies/snap-divergence/results/prd-candidate-results.jsonl")
DEFAULT_COMPARISON_RESULTS = Path("studies/snap-divergence/results/comparison-candidate-results.jsonl")
DEFAULT_REPORT = Path("studies/snap-divergence/REPORT.md")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def compare_result_sets(
    policyengine_results: Iterable[dict[str, Any]],
    prd_results: Iterable[dict[str, Any]],
    *,
    tolerance: Decimal = Decimal("1.00"),
) -> list[dict[str, Any]]:
    policyengine_by_case = {result["caseId"]: result for result in policyengine_results}
    prd_by_case = {result["caseId"]: result for result in prd_results}
    missing_policyengine = sorted(set(prd_by_case) - set(policyengine_by_case))
    missing_prd = sorted(set(policyengine_by_case) - set(prd_by_case))
    if missing_policyengine or missing_prd:
        raise ValueError(
            f"case id mismatch: missing_policyengine={missing_policyengine} missing_prd={missing_prd}",
        )
    return [
        compare_pair(policyengine_by_case[case_id], prd_by_case[case_id], tolerance=tolerance)
        for case_id in sorted(policyengine_by_case)
    ]


def compare_pair(
    policyengine: dict[str, Any],
    prd: dict[str, Any],
    *,
    tolerance: Decimal = Decimal("1.00"),
) -> dict[str, Any]:
    pe_eligible = bool(policyengine["outputs"]["us-snap/decision.eligible"]["value"])
    prd_eligible = bool(prd["outputs"]["us-snap/decision.eligible"]["value"])
    pe_allotment = _money(policyengine)
    prd_allotment = _money(prd)
    difference = abs(pe_allotment - prd_allotment)
    eligible_agrees = pe_eligible == prd_eligible
    allotment_agrees = difference <= tolerance
    agreement = eligible_agrees and allotment_agrees
    decision_relevant = (not eligible_agrees) or difference > Decimal("10.00")

    return {
        "caseId": policyengine["caseId"],
        "agreement": agreement,
        "classification": "agreement" if agreement else "unclassified",
        "decisionRelevant": decision_relevant,
        "policyengine": {
            "eligible": pe_eligible,
            "allotment": _decimal_string(pe_allotment),
        },
        "prd": {
            "eligible": prd_eligible,
            "allotment": _decimal_string(prd_allotment),
            "annualSnapValue": prd.get("rawOutputs", {}).get("snapValueAnnual"),
        },
        "allotmentDifference": _decimal_string(difference),
        "tolerance": _decimal_string(tolerance),
        "evidence": [
            "PolicyEngine result: studies/snap-divergence/results/policyengine-candidate-results.jsonl",
            "PRD result: studies/snap-divergence/results/prd-candidate-results.jsonl",
        ],
    }


def summarize_comparisons(comparisons: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(comparisons),
        "agreements": sum(1 for item in comparisons if item["agreement"]),
        "divergences": sum(1 for item in comparisons if not item["agreement"]),
        "decisionRelevant": sum(1 for item in comparisons if item["decisionRelevant"]),
        "unclassified": sum(1 for item in comparisons if item["classification"] == "unclassified"),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def write_report(path: Path, comparisons: list[dict[str, Any]]) -> None:
    summary = summarize_comparisons(comparisons)
    divergent = [item for item in comparisons if not item["agreement"]]
    lines = [
        "# SNAP Divergence Draft Report",
        "",
        "This draft is generated from candidate fixtures. It is not a final finding report until fixtures are promoted and divergences are classified.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Total cases | {summary['total']} |",
        f"| Agreements | {summary['agreements']} |",
        f"| Divergences | {summary['divergences']} |",
        f"| Decision-relevant divergences | {summary['decisionRelevant']} |",
        f"| Unclassified divergences | {summary['unclassified']} |",
        "",
        "## Divergences",
        "",
    ]
    if not divergent:
        lines.append("No divergences exceeded the configured tolerance.")
    else:
        lines.extend(
            [
                "| Case | PolicyEngine allotment | PRD allotment | Difference | Decision-relevant | Classification |",
                "|---|---:|---:|---:|---|---|",
            ],
        )
        for item in divergent:
            lines.append(
                f"| `{item['caseId']}` | {item['policyengine']['allotment']} | "
                f"{item['prd']['allotment']} | {item['allotmentDifference']} | "
                f"{str(item['decisionRelevant']).lower()} | {item['classification']} |",
            )
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            "- PolicyEngine candidate outputs: `studies/snap-divergence/results/policyengine-candidate-results.jsonl`",
            "- PRD candidate outputs: `studies/snap-divergence/results/prd-candidate-results.jsonl`",
            "- Machine-readable comparison rows: `studies/snap-divergence/results/comparison-candidate-results.jsonl`",
        ],
    )
    path.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policyengine", type=Path, default=DEFAULT_POLICYENGINE_RESULTS)
    parser.add_argument("--prd", type=Path, default=DEFAULT_PRD_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_COMPARISON_RESULTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)

    comparisons = compare_result_sets(load_jsonl(args.policyengine), load_jsonl(args.prd))
    write_jsonl(args.output, comparisons)
    write_report(args.report, comparisons)
    return 0


def _money(result: dict[str, Any]) -> Decimal:
    return Decimal(str(result["outputs"]["us-snap/decision.allotment"]["value"]))


def _decimal_string(value: Decimal) -> str:
    normalized = value.normalize()
    return format(normalized, "f") if normalized else "0"


if __name__ == "__main__":
    raise SystemExit(main())
