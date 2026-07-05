"""PolicyEngine-US runner for SNAP divergence fixtures."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from policyengine_trace import project_flat_trace

POLICYENGINE_VERSION = "1.755.5"
POLICYENGINE_COMMIT = "fc64cef64ab55c3c48309c7fb304c35e5f3c9184"
DEFAULT_PERIOD = "2026-01"
DEFAULT_FIXTURE_PATH = Path(
    "studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json",
)


class PolicyEngineUnavailable(RuntimeError):
    """Raised when the pinned PolicyEngine runtime is not importable."""


def load_cases(path: str | Path, *, case_ids: Iterable[str] | None = None) -> list[dict[str, Any]]:
    fixture_file = Path(path)
    data = json.loads(fixture_file.read_text())
    cases = data["cases"]
    if case_ids is None:
        return cases
    wanted = set(case_ids)
    return [case for case in cases if case["caseId"] in wanted]


def build_policyengine_situation(case: dict[str, Any]) -> dict[str, Any]:
    inputs = case["inputs"]
    period_year = case["period"][:4]
    household = case["entities"]["household"]
    ages = _parse_ages(inputs["us-snap/variable.person_ages"]["value"])
    members = _member_names(ages)
    earned_income = monthly_money(inputs["us-snap/variable.earned_income_monthly"], "earned")
    unearned_income = monthly_money(inputs["us-snap/variable.unearned_income_monthly"], "unearned")
    dependent_care = monthly_money(
        inputs["us-snap/variable.dependent_care_expense_monthly"],
        "dependent care",
    )
    medical = monthly_money(inputs["us-snap/variable.medical_expense_monthly"], "medical")
    shelter = monthly_money(inputs["us-snap/variable.shelter_expense_monthly"], "shelter")
    utility = monthly_money(inputs["us-snap/variable.utility_expense_monthly"], "utility")
    assets = monthly_money(inputs["us-snap/variable.countable_assets"], "assets")
    has_elderly_disabled = bool(
        inputs["us-snap/variable.has_elderly_disabled"].get("value", False),
    )

    people: dict[str, Any] = {}
    for index, (name, age) in enumerate(zip(members, ages, strict=True)):
        is_child = age < 18
        people[name] = {
            "age": {period_year: age},
            "is_tax_unit_head": {period_year: index == 0},
            "is_tax_unit_spouse": {period_year: index == 1 and not is_child},
            "is_tax_unit_dependent": {period_year: is_child},
            "is_disabled": {period_year: has_elderly_disabled and index == 1},
            "immigration_status_str": {period_year: "CITIZEN"},
            "employment_income": {period_year: float(_annualize(earned_income if index == 0 else Decimal("0")))},
            "snap_allowable_medical_expenses": {
                period_year: float(_annualize(medical if index == 0 else Decimal("0"))),
            },
        }

    spm_unit = {
        "members": members,
        "snap_unearned_income": {period_year: float(_annualize(unearned_income))},
        "childcare_expenses": {period_year: float(_annualize(dependent_care))},
        "housing_cost": {period_year: float(_annualize(shelter))},
        "heating_cooling_expense": {period_year: float(_annualize(utility))},
        "has_heating_cooling_expense": {period_year: utility > 0},
        "phone_expense": {period_year: float(_annualize(utility))},
        "has_phone_expense": {period_year: utility > 0},
        "snap_assets": {period_year: float(assets)},
        "snap_emergency_allotment": {period_year: 0.0},
    }

    return {
        "people": people,
        "households": {
            "household": {
                "members": members,
                "state_code_str": household["state"],
            },
        },
        "spm_units": {"spm_unit": spm_unit},
        "tax_units": {
            "tax_unit": {
                "members": members,
                "tax_unit_is_joint": {period_year: len([age for age in ages if age >= 18]) >= 2},
            },
        },
        "families": {"family": {"members": members}},
        "marital_units": _marital_units(members, ages),
    }


def run_policyengine_case(case: dict[str, Any], *, include_trace: bool = True) -> dict[str, Any]:
    simulation_class = _load_policyengine_simulation()
    if simulation_class is None:
        raise PolicyEngineUnavailable(
            "policyengine_us is not importable; run with .venv-policyengine or install the pinned editable checkout",
        )

    period = case.get("period", DEFAULT_PERIOD)
    simulation = simulation_class(situation=build_policyengine_situation(case), trace=include_trace)
    eligible = _scalar(simulation.calculate("is_snap_eligible", period))
    allotment = Decimal(str(_scalar(simulation.calculate("snap", period))))
    trace = _project_trace(simulation, case["caseId"], period) if include_trace else None

    return format_run_result(
        case_id=case["caseId"],
        period=period,
        eligible=bool(eligible),
        allotment=allotment,
        trace=trace,
    )


def format_run_result(
    *,
    case_id: str,
    period: str,
    eligible: bool,
    allotment: Decimal,
    trace: dict[str, Any] | None,
) -> dict[str, Any]:
    result = {
        "caseId": case_id,
        "period": period,
        "engine": {
            "name": "policyengine-us",
            "version": POLICYENGINE_VERSION,
            "commit": POLICYENGINE_COMMIT,
        },
        "outputs": {
            "us-snap/decision.eligible": {"value": eligible, "valueState": "known"},
            "us-snap/decision.allotment": {
                "value": _decimal_string(allotment),
                "valueState": "known",
                "currency": "USD",
                "tolerance": "1.00",
            },
        },
    }
    if trace is not None:
        result["trace"] = trace
    return result


def monthly_money(value_object: dict[str, Any], label: str) -> Decimal:
    if "value" not in value_object:
        raise ValueError(f"money input missing value: {label}")
    return Decimal(str(value_object["value"]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURE_PATH)
    parser.add_argument("--case-id", action="append", dest="case_ids")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--no-trace", action="store_true")
    args = parser.parse_args(argv)

    cases = load_cases(args.fixtures, case_ids=args.case_ids)
    results = [
        run_policyengine_case(case, include_trace=not args.no_trace)
        for case in cases
    ]
    write_results(args.output, results)
    return 0


def write_results(path: Path, results: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jsonl":
        path.write_text("".join(json.dumps(result, sort_keys=True) + "\n" for result in results))
        return
    path.write_text(json.dumps({"results": results}, indent=2) + "\n")


def _load_policyengine_simulation() -> Any:
    try:
        from policyengine_us import Simulation
    except ImportError:
        return None
    return Simulation


def _project_trace(simulation: Any, case_id: str, period: str) -> dict[str, Any] | None:
    flat_trace = simulation.tracer.get_serialized_flat_trace()
    output_key = f"snap<{period}, (default)>"
    if output_key not in flat_trace:
        return None
    return project_flat_trace(
        flat_trace,
        output_key=output_key,
        case_id=case_id,
        package_id="policyengine-us",
        package_version=POLICYENGINE_VERSION,
        engine_version=POLICYENGINE_VERSION,
        timestamp=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        namespace="us-snap",
    )


def _parse_ages(value: Any) -> list[int]:
    text = str(value)
    if text.startswith("ages:"):
        text = text.removeprefix("ages:")
    return [int(part) for part in text.replace(",", "|").split("|") if part]


def _member_names(ages: list[int]) -> list[str]:
    adult_count = 0
    child_count = 0
    names = []
    for age in ages:
        if not names:
            names.append("head")
        elif age < 18:
            child_count += 1
            names.append(f"child{child_count}")
        else:
            adult_count += 1
            names.append("spouse" if adult_count == 1 else f"adult{adult_count}")
    return names


def _marital_units(members: list[str], ages: list[int]) -> dict[str, Any]:
    adults = [member for member, age in zip(members, ages, strict=True) if age >= 18]
    children = [member for member, age in zip(members, ages, strict=True) if age < 18]
    marital_units: dict[str, Any] = {}
    if len(adults) >= 2:
        marital_units["mu_couple"] = {"members": adults[:2]}
        for adult in adults[2:]:
            marital_units[f"mu_{adult}"] = {"members": [adult]}
    elif adults:
        marital_units[f"mu_{adults[0]}"] = {"members": [adults[0]]}
    for child in children:
        marital_units[f"mu_{child}"] = {"members": [child]}
    return marital_units


def _annualize(monthly: Decimal) -> Decimal:
    return monthly * Decimal("12")


def _scalar(value: Any) -> Any:
    if hasattr(value, "tolist"):
        value = value.tolist()
    if isinstance(value, list) and len(value) == 1:
        return value[0]
    return value


def _decimal_string(value: Decimal) -> str:
    return format(value.normalize(), "f") if value else "0"


if __name__ == "__main__":
    raise SystemExit(main())
