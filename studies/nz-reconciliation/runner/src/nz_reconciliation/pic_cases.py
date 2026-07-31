"""Convert inventory cases into PIC-shaped fixture cases for the Axiom harness."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


def _decimal_string(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return str(value)
    text = format(number, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _value_object(value: Any, *, currency: str | None = "NZD") -> dict[str, Any]:
    if isinstance(value, bool):
        return {"value": value, "valueState": "known"}
    payload: dict[str, Any] = {
        "value": _decimal_string(value),
        "valueState": "known",
    }
    if currency is not None and not isinstance(value, bool):
        # Rates and dimensionless counts still get currency omitted when clearly ratios.
        text = str(value)
        if "." in text and Decimal(text) < 1 and Decimal(text) > 0:
            payload.pop("currency", None)
        else:
            payload["currency"] = currency
    return payload


def _short_id(rulespec_id: str, *, kind: str) -> str:
    """Map durable RuleSpec IDs to the harness PIC short IDs used by adapters."""
    # Example:
    # nz:statutes/income_tax/schedule_1/individual_income_tax#input.taxable_income
    # -> nz-income-tax/variable.taxable_income
    if "#" not in rulespec_id:
        return rulespec_id
    module, local = rulespec_id.split("#", 1)
    local_name = local.split(".", 1)[-1]
    if module.endswith("/individual_income_tax"):
        prefix = "nz-income-tax"
    elif module.endswith("/earners_levy"):
        prefix = "nz-acc"
    elif module.endswith("/contributions"):
        prefix = "nz-kiwisaver"
    else:
        prefix = "nz-unknown"
    middle = "variable" if kind == "input" else "decision"
    return f"{prefix}/{middle}.{local_name}"


# Derived outputs exposed by axiom-rules-engine compile for these modules
# (parameter lookups like bracket thresholds/rates are not derived outputs).
DERIVED_OUTPUT_LOCAL_NAMES: dict[str, frozenset[str]] = {
    "income_tax": frozenset({"individual_income_tax_before_credits"}),
    "acc_earners_levy": frozenset(
        {
            "acc_standard_earners_levy_excluding_gst",
            "acc_standard_earners_levy_including_gst",
            "acc_low_self_employed_minimum_levy_excluding_gst",
            "acc_weekly_compensation_purchase_levy_excluding_gst",
            "acc_self_employed_invoice_levy_payable_after_exempt_amount",
        }
    ),
    "kiwisaver": frozenset(
        {
            "kiwisaver_employee_deduction",
            "kiwisaver_minimum_employer_contribution",
        }
    ),
}


def inventory_case_to_pic_case(
    case: dict[str, Any],
    *,
    derived_only: bool = True,
) -> dict[str, Any]:
    """Build a PIC fixture case from an inventory case."""
    inputs = {
        _short_id(key, kind="input"): _value_object(value)
        for key, value in (case.get("inputs") or {}).items()
    }
    expected_items = list((case.get("expectedRulespec") or {}).items())
    if derived_only:
        allowed = DERIVED_OUTPUT_LOCAL_NAMES.get(str(case.get("domain")), frozenset())
        expected_items = [
            (key, value) for key, value in expected_items if key.rsplit("#", 1)[-1] in allowed
        ]
    expected = {
        _short_id(key, kind="output"): _value_object(value) for key, value in expected_items
    }
    return {
        "caseId": case["caseId"],
        "description": case.get("name") or case["caseId"],
        "period": case.get("period"),
        "domain": case.get("domain"),
        "entities": {"person": {"type": "Person", "id": "person:1"}},
        "inputs": inputs,
        "expected": expected,
        "sourceRefs": list(case.get("sourceRefs") or []),
        "provenance": {
            "curator": "nz_reconciliation Phase 2 runner",
            "method": "mechanical",
            "source": (case.get("rulespec") or {}).get("testPath"),
            "interpreterOfRecord": "TheAxiomFoundation/rulespec-nz",
            "disclaimer": (
                "Inventory-derived mechanical fixture for cross-engine reconciliation; "
                "not a promoted legal oracle."
            ),
        },
    }
