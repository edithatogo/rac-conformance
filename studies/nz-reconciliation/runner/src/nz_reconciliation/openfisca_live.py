"""Live OpenFisca Aotearoa simulation for NZ reconciliation cases.

Requires a working country package install (typically Python 3.11 +
openfisca-core 41.x + the feat/199 branch of openfisca-aotearoa).
"""

from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from nz_reconciliation.comparison import write_jsonl
from nz_reconciliation.inventory import DEFAULT_INVENTORY, load_inventory, select_cases

DEFAULT_OUTPUT = Path(
    "studies/nz-reconciliation/results/openfisca-aotearoa-live-results.jsonl",
)


def _money_string(value: float | int | Decimal) -> str:
    number = Decimal(str(value))
    text = format(number, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _taxable_income(case: dict[str, Any]) -> Decimal | None:
    for key, raw in (case.get("inputs") or {}).items():
        if key.endswith("taxable_income") or key.endswith("#input.taxable_income"):
            try:
                return Decimal(str(raw))
            except (InvalidOperation, ValueError):
                return None
    return None


def _acc_earnings(case: dict[str, Any]) -> Decimal | None:
    for key, raw in (case.get("inputs") or {}).items():
        if "acc_earnings" in key or "earners_levy" in key and "input" in key:
            try:
                return Decimal(str(raw))
            except (InvalidOperation, ValueError):
                return None
    # some cases use full path
    for key, raw in (case.get("inputs") or {}).items():
        if "acc_earnings_for_earners_levy" in key:
            try:
                return Decimal(str(raw))
            except (InvalidOperation, ValueError):
                return None
    return None


def _ks_salary(case: dict[str, Any]) -> Decimal | None:
    for key, raw in (case.get("inputs") or {}).items():
        if "kiwisaver_gross_salary" in key or "gross_salary_or_wages" in key:
            try:
                return Decimal(str(raw))
            except (InvalidOperation, ValueError):
                return None
    return None


def _period_year(case: dict[str, Any]) -> str:
    period = case.get("period") or ""
    # "2026-04-01/2027-03-31" -> use 2026 for OF calendar year (April lookup in formula)
    if isinstance(period, str) and len(period) >= 4 and period[:4].isdigit():
        return period[:4]
    meta = case.get("periodMeta") or {}
    start = meta.get("start") or ""
    if isinstance(start, str) and len(start) >= 4:
        return start[:4]
    return "2026"


def run_openfisca_live_case(case: dict[str, Any], system: Any) -> dict[str, Any]:
    """Run one inventory case against a loaded TaxBenefitSystem."""
    from openfisca_core.simulations import SimulationBuilder

    domain = case.get("domain")
    year = _period_year(case)
    person: dict[str, Any] = {}
    outputs: dict[str, Any] = {}
    status = "ok"
    notes = "live SimulationBuilder run"

    try:
        if domain == "income_tax":
            income = _taxable_income(case)
            if income is None:
                return _gap_row(case, "no taxable_income input")
            person["income_tax__taxable_income"] = {year: float(income)}
            sim = SimulationBuilder().build_from_entities(
                system,
                {"persons": {"person": person}},
            )
            value = float(sim.calculate("income_tax__schedule_1_tax_before_credits", year)[0])
            outputs["individual_income_tax_before_credits"] = {
                "value": _money_string(value),
                "valueState": "known",
                "currency": "NZD",
            }
        elif domain == "acc_earners_levy":
            earnings = _acc_earnings(case)
            if earnings is None:
                # self-employed cases may need different vars — mark partial
                return _gap_row(case, "no standard acc earnings input (self-employed path not mapped)")
            person["acc__earnings_for_earners_levy"] = {year: float(earnings)}
            sim = SimulationBuilder().build_from_entities(
                system,
                {"persons": {"person": person}},
            )
            value = float(sim.calculate("acc__earners_levy_including_gst", year)[0])
            outputs["acc_standard_earners_levy_including_gst"] = {
                "value": _money_string(value),
                "valueState": "known",
                "currency": "NZD",
            }
        elif domain == "kiwisaver":
            salary = _ks_salary(case)
            if salary is None:
                return _gap_row(case, "no kiwisaver salary input (parameter-only case)")
            person["kiwisaver__gross_salary_or_wages"] = {year: float(salary)}
            sim = SimulationBuilder().build_from_entities(
                system,
                {"persons": {"person": person}},
            )
            emp = float(sim.calculate("kiwisaver__employee_minimum_contribution", year)[0])
            er = float(sim.calculate("kiwisaver__employer_minimum_contribution", year)[0])
            outputs["kiwisaver_employee_deduction"] = {
                "value": _money_string(emp),
                "valueState": "known",
                "currency": "NZD",
            }
            outputs["kiwisaver_minimum_employer_contribution"] = {
                "value": _money_string(er),
                "valueState": "known",
                "currency": "NZD",
            }
        else:
            return _gap_row(case, f"unknown domain {domain}")
    except Exception as exc:  # noqa: BLE001 - surface engine failures in result row
        status = "runtime_error"
        notes = f"{type(exc).__name__}: {exc}"
        outputs = {}

    return {
        "caseId": case["caseId"],
        "domain": domain,
        "engine": "openfisca-aotearoa",
        "status": status,
        "method": "live-simulation",
        "period": case.get("period"),
        "periodYear": year,
        "outputs": outputs,
        "notes": notes,
        "sourceRefs": ["https://github.com/BetterRules/openfisca-aotearoa/pull/200"],
    }


def _gap_row(case: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "caseId": case["caseId"],
        "domain": case.get("domain"),
        "engine": "openfisca-aotearoa",
        "status": "engine_gap",
        "method": "live-simulation",
        "period": case.get("period"),
        "outputs": {},
        "gapReason": reason,
        "notes": reason,
        "sourceRefs": ["https://github.com/BetterRules/openfisca-aotearoa/pull/200"],
    }


def run_openfisca_live_suite(
    inventory_path: Path | None = None,
    *,
    include_blocked: bool = True,
) -> list[dict[str, Any]]:
    from openfisca_aotearoa import CountryTaxBenefitSystem

    inventory = load_inventory(inventory_path or DEFAULT_INVENTORY)
    cases = select_cases(inventory, include_blocked=include_blocked)
    system = CountryTaxBenefitSystem()
    return [run_openfisca_live_case(case, system) for case in cases]


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Live OpenFisca Aotearoa NZ recon runner.")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--exclude-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        rows = run_openfisca_live_suite(
            args.inventory,
            include_blocked=not args.exclude_blocked,
        )
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, indent=2))
        return 2

    write_jsonl(args.output, rows)
    ok = sum(1 for r in rows if r["status"] == "ok")
    print(
        json.dumps(
            {
                "ok": True,
                "cases": len(rows),
                "live_ok": ok,
                "gaps_or_errors": len(rows) - ok,
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
