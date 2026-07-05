"""Atlanta Fed PRD SNAP runner for divergence fixtures."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from decimal import Decimal
from pathlib import Path
from typing import Any

from snap_divergence.policyengine_runner import load_cases, monthly_money

PRD_COMMIT = "1d8e8674563a7653ec707d18956faa14b016bc5b"
DEFAULT_PRD_REPO = Path(".external-repos/policy-rules-database")
DEFAULT_FIXTURE_PATH = Path(
    "studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json",
)
R_BRIDGE = Path(__file__).resolve().parents[2] / "R" / "prd_snap_runner.R"


class PRDRunnerError(RuntimeError):
    """Raised when the PRD R bridge fails."""


def build_prd_row(case: dict[str, Any]) -> dict[str, Any]:
    inputs = case["inputs"]
    household = case["entities"]["household"]
    ages = _parse_ages(inputs["us-snap/variable.person_ages"]["value"])
    has_elderly_disabled = bool(
        inputs["us-snap/variable.has_elderly_disabled"].get("value", False),
    )
    earned = monthly_money(inputs["us-snap/variable.earned_income_monthly"], "earned")
    unearned = monthly_money(inputs["us-snap/variable.unearned_income_monthly"], "unearned")
    dependent_care = monthly_money(
        inputs["us-snap/variable.dependent_care_expense_monthly"],
        "dependent care",
    )
    medical = monthly_money(inputs["us-snap/variable.medical_expense_monthly"], "medical")
    shelter = monthly_money(inputs["us-snap/variable.shelter_expense_monthly"], "shelter")
    utility = monthly_money(inputs["us-snap/variable.utility_expense_monthly"], "utility")
    assets = monthly_money(inputs["us-snap/variable.countable_assets"], "assets")

    row: dict[str, Any] = {
        "caseId": case["caseId"],
        "period": case["period"],
        "ruleYear": int(case["period"][:4]),
        "stateFIPS": int(household["stateFips"]),
        "famsize": int(inputs["us-snap/variable.snap_unit_size"]["value"]),
        "income": float(_annualize(earned)),
        "income.gift": float(_annualize(unearned)),
        "income.child_support": 0.0,
        "income.investment": 0.0,
        "value.tanf": 0.0,
        "value.ssi": 0.0,
        "value.ssdi": 0.0,
        "netexp.childcare": float(_annualize(dependent_care)),
        "oop.add_for_elderlyordisabled": float(_annualize(medical)),
        "netexp.rentormortgage": float(_annualize(shelter)),
        "netexp.utilities": float(_annualize(utility)),
        "assets.cash": float(assets),
        "assets.car1": 0.0,
        "totalassets": float(assets),
    }
    for index in range(1, 13):
        row[f"agePerson{index}"] = ages[index - 1] if index <= len(ages) else None
        row[f"disability{index}"] = 1 if has_elderly_disabled and index == 2 else 0
    for index in range(1, 7):
        row[f"value.ssiAdlt{index}"] = 0.0
        row[f"ssdiPIA{index}"] = 0.0
        row[f"value.ssiChild{index}"] = 0.0
    return row


def run_prd_cases(
    cases: list[dict[str, Any]],
    *,
    prd_repo: Path = DEFAULT_PRD_REPO,
    rscript: str = "Rscript",
) -> list[dict[str, Any]]:
    rows = [build_prd_row(case) for case in cases]
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = Path(temp_dir) / "prd-input.json"
        output_path = Path(temp_dir) / "prd-output.jsonl"
        input_path.write_text(json.dumps(rows, indent=2) + "\n")
        command = [
            rscript,
            str(R_BRIDGE),
            str(prd_repo),
            str(input_path),
            str(output_path),
        ]
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            raise PRDRunnerError(
                f"PRD runner failed with exit {completed.returncode}: {completed.stderr.strip()}",
            )
        return [json.loads(line) for line in output_path.read_text().splitlines()]


def format_prd_result(case_id: str, period: str, *, annual_snap_value: float | int | str) -> dict[str, Any]:
    annual = Decimal(str(annual_snap_value))
    monthly = annual / Decimal("12")
    return {
        "caseId": case_id,
        "period": period,
        "engine": {
            "name": "atlanta-fed-prd",
            "commit": PRD_COMMIT,
            "adapter": "direct-function.snapBenefit",
        },
        "outputs": {
            "us-snap/decision.eligible": {
                "value": annual > 0,
                "valueState": "known",
            },
            "us-snap/decision.allotment": {
                "value": _decimal_string(monthly),
                "valueState": "known",
                "currency": "USD",
                "tolerance": "1.00",
            },
        },
        "rawOutputs": {"snapValueAnnual": _decimal_string(annual)},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURE_PATH)
    parser.add_argument("--case-id", action="append", dest="case_ids")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prd-repo", type=Path, default=DEFAULT_PRD_REPO)
    args = parser.parse_args(argv)

    cases = load_cases(args.fixtures, case_ids=args.case_ids)
    results = run_prd_cases(cases, prd_repo=args.prd_repo)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(result, sort_keys=True) + "\n" for result in results))
    return 0


def _parse_ages(value: Any) -> list[int]:
    text = str(value)
    if text.startswith("ages:"):
        text = text.removeprefix("ages:")
    return [int(part) for part in text.replace(",", "|").split("|") if part]


def _annualize(monthly: Decimal) -> Decimal:
    return monthly * Decimal("12")


def _decimal_string(value: Decimal) -> str:
    normalized = value.normalize()
    return format(normalized, "f") if normalized else "0"


if __name__ == "__main__":
    raise SystemExit(main())
