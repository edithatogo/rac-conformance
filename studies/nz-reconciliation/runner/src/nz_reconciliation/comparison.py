"""Compare RuleSpec and OpenFisca Aotearoa result JSONL rows."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

DEFAULT_RULESPEC_RESULTS = Path(
    "studies/nz-reconciliation/results/rulespec-candidate-results.jsonl",
)
DEFAULT_OPENFISCA_RESULTS = Path(
    "studies/nz-reconciliation/results/openfisca-aotearoa-candidate-results.jsonl",
)
DEFAULT_COMPARISON_RESULTS = Path(
    "studies/nz-reconciliation/results/comparison-candidate-results.jsonl",
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load a JSONL results file."""
    if not path.exists():
        return []
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def _decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _decimal_string(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _primary_numeric(outputs: dict[str, Any]) -> Decimal | None:
    """Pick the first numeric output value for pairwise comparison."""
    for payload in outputs.values():
        if isinstance(payload, dict) and "value" in payload:
            number = _decimal(payload.get("value"))
            if number is not None:
                return number
        number = _decimal(payload)
        if number is not None:
            return number
    return None


def compare_pair(
    rulespec: dict[str, Any],
    openfisca: dict[str, Any],
    *,
    tolerance: Decimal = Decimal("0.01"),
) -> dict[str, Any]:
    """Compare one RuleSpec result row with one OpenFisca result row."""
    case_id = rulespec.get("caseId") or openfisca.get("caseId")
    rs_outputs = rulespec.get("outputs") or {}
    of_outputs = openfisca.get("outputs") or {}
    rs_status = rulespec.get("status", "ok")
    of_status = openfisca.get("status", "ok")
    rs_value = _primary_numeric(rs_outputs)
    of_value = _primary_numeric(of_outputs)

    evidence = [
        "RuleSpec result JSONL",
        "OpenFisca Aotearoa result JSONL",
    ]
    evidence.extend(openfisca.get("evidence") or [])
    evidence.extend(rulespec.get("evidence") or [])

    # Non-executable sides are classified, not treated as numeric disagreement.
    if of_status == "engine_gap":
        agreement = False
        classification = "engine_gap"
        difference = None
    elif rs_status in {"blocked_compile", "compile_blocked", "adapter_failure"}:
        agreement = False
        classification = str(rs_status)
        difference = None
    elif rs_value is None or of_value is None:
        agreement = rs_outputs == of_outputs and rs_outputs != {}
        difference = None
        classification = "agreement" if agreement else "unclassified"
    else:
        difference = abs(rs_value - of_value)
        agreement = difference <= tolerance
        classification = "agreement" if agreement else "unclassified"

    return {
        "caseId": case_id,
        "domain": rulespec.get("domain") or openfisca.get("domain"),
        "agreement": agreement,
        "classification": classification,
        "rulespec": {
            "status": rs_status,
            "primaryValue": None if rs_value is None else _decimal_string(rs_value),
            "outputs": rs_outputs,
        },
        "openfiscaAotearoa": {
            "status": of_status,
            "primaryValue": None if of_value is None else _decimal_string(of_value),
            "outputs": of_outputs,
            "notes": openfisca.get("notes"),
        },
        "valueDifference": None if difference is None else _decimal_string(difference),
        "tolerance": _decimal_string(tolerance),
        "evidence": evidence,
    }


def compare_result_sets(
    rulespec_results: Iterable[dict[str, Any]],
    openfisca_results: Iterable[dict[str, Any]],
    *,
    tolerance: Decimal = Decimal("0.01"),
) -> list[dict[str, Any]]:
    """Compare two result sets keyed by caseId."""
    rulespec_by_case = {result["caseId"]: result for result in rulespec_results}
    openfisca_by_case = {result["caseId"]: result for result in openfisca_results}
    missing_rulespec = sorted(set(openfisca_by_case) - set(rulespec_by_case))
    missing_openfisca = sorted(set(rulespec_by_case) - set(openfisca_by_case))
    if missing_rulespec or missing_openfisca:
        msg = (
            "case id mismatch: "
            f"missing_rulespec={missing_rulespec} missing_openfisca={missing_openfisca}"
        )
        raise ValueError(msg)
    return [
        compare_pair(rulespec_by_case[case_id], openfisca_by_case[case_id], tolerance=tolerance)
        for case_id in sorted(rulespec_by_case)
    ]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write comparison rows as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for pairwise comparison."""
    parser = argparse.ArgumentParser(
        description="Compare RuleSpec and OpenFisca Aotearoa NZ reconciliation results.",
    )
    parser.add_argument("--rulespec", type=Path, default=DEFAULT_RULESPEC_RESULTS)
    parser.add_argument("--openfisca", type=Path, default=DEFAULT_OPENFISCA_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_COMPARISON_RESULTS)
    parser.add_argument("--tolerance", default="0.01")
    args = parser.parse_args(argv)

    rulespec_results = load_jsonl(args.rulespec)
    openfisca_results = load_jsonl(args.openfisca)
    if not rulespec_results or not openfisca_results:
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "missing_result_files",
                    "rulespec_count": len(rulespec_results),
                    "openfisca_count": len(openfisca_results),
                    "hint": "Run Phase 2 engine runners to produce candidate JSONL files first.",
                },
                indent=2,
            )
        )
        return 2

    rows = compare_result_sets(
        rulespec_results,
        openfisca_results,
        tolerance=Decimal(args.tolerance),
    )
    write_jsonl(args.output, rows)
    agreed = sum(1 for row in rows if row["agreement"])
    print(
        json.dumps(
            {
                "ok": True,
                "cases": len(rows),
                "agreements": agreed,
                "divergences": len(rows) - agreed,
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
