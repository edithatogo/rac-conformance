"""Deterministic adapters for Axiom RuleSpec execution requests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any


@dataclass(frozen=True)
class RuleSpecTarget:
    """A public RuleSpec corpus target for the harness."""

    repo: str
    repo_commit: str
    module_path: str
    test_path: str
    module_id: str


RULESPEC_NZ_GST_TARGET = RuleSpecTarget(
    repo="TheAxiomFoundation/rulespec-nz",
    repo_commit="3c6436b2ecf82dd7a7f7810a406a2695a64af33a",
    module_path="nz/statutes/gst/rate.yaml",
    test_path="nz/statutes/gst/rate.test.yaml",
    module_id="nz:statutes/gst/rate",
)


RULESPEC_NZ_ACC_EARNERS_LEVY_TARGET = RuleSpecTarget(
    repo="TheAxiomFoundation/rulespec-nz",
    repo_commit="3c6436b2ecf82dd7a7f7810a406a2695a64af33a",
    module_path="nz/regulations/acc/earners_levy.yaml",
    test_path="nz/regulations/acc/earners_levy.test.yaml",
    module_id="nz:regulations/acc/earners_levy",
)


RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_TARGET = RuleSpecTarget(
    repo="TheAxiomFoundation/rulespec-nz",
    repo_commit="3c6436b2ecf82dd7a7f7810a406a2695a64af33a",
    module_path="nz/statutes/income_tax/schedule_1/individual_income_tax.yaml",
    test_path="nz/statutes/income_tax/schedule_1/individual_income_tax.test.yaml",
    module_id="nz:statutes/income_tax/schedule_1/individual_income_tax",
)


RULESPEC_NZ_GST_INPUTS = {
    "nz-gst/variable.gst_exclusive_amount": "nz:statutes/gst/rate#input.gst_exclusive_amount",
    "nz-gst/variable.gst_inclusive_amount": "nz:statutes/gst/rate#input.gst_inclusive_amount",
    "nz-gst/variable.gst_imported_goods_value": "nz:statutes/gst/rate#input.gst_imported_goods_value",
    "nz-gst/variable.gst_imported_goods_outside_new_zealand_at_supply": (
        "nz:statutes/gst/rate#input.gst_imported_goods_outside_new_zealand_at_supply"
    ),
    "nz-gst/variable.gst_imported_goods_delivered_to_new_zealand_address": (
        "nz:statutes/gst/rate#input.gst_imported_goods_delivered_to_new_zealand_address"
    ),
}


RULESPEC_NZ_ACC_EARNERS_LEVY_INPUTS = {
    "nz-acc/variable.acc_earnings_for_earners_levy": (
        "nz:regulations/acc/earners_levy#input.acc_earnings_for_earners_levy"
    ),
    "nz-acc/variable.acc_self_employed_more_than_30_hours_per_week": (
        "nz:regulations/acc/earners_levy#input.acc_self_employed_more_than_30_hours_per_week"
    ),
    "nz-acc/variable.acc_self_employed_earnings_for_earners_levy": (
        "nz:regulations/acc/earners_levy#input.acc_self_employed_earnings_for_earners_levy"
    ),
    "nz-acc/variable.acc_employee_earnings_for_low_self_employed_formula": (
        "nz:regulations/acc/earners_levy#input.acc_employee_earnings_for_low_self_employed_formula"
    ),
    "nz-acc/variable.acc_self_employed_purchases_weekly_compensation": (
        "nz:regulations/acc/earners_levy#input.acc_self_employed_purchases_weekly_compensation"
    ),
    "nz-acc/variable.acc_agreed_weekly_compensation_purchased_annual_amount": (
        "nz:regulations/acc/earners_levy#input.acc_agreed_weekly_compensation_purchased_annual_amount"
    ),
    "nz-acc/variable.acc_invoice_issued_to_self_employed_person_for_acc_act_purposes": (
        "nz:regulations/acc/earners_levy#input.acc_invoice_issued_to_self_employed_person_for_acc_act_purposes"
    ),
    "nz-acc/variable.acc_invoice_includes_earners_levy": (
        "nz:regulations/acc/earners_levy#input.acc_invoice_includes_earners_levy"
    ),
    "nz-acc/variable.acc_self_employed_invoice_acc_levy_amount": (
        "nz:regulations/acc/earners_levy#input.acc_self_employed_invoice_acc_levy_amount"
    ),
}


RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_INPUTS = {
    "nz-income-tax/variable.taxable_income": (
        "nz:statutes/income_tax/schedule_1/individual_income_tax#input.taxable_income"
    ),
    "nz-income-tax/variable.bracket": (
        "nz:statutes/income_tax/schedule_1/individual_income_tax#input.bracket"
    ),
}


RULESPEC_NZ_GST_OUTPUTS = {
    "nz-gst/decision.gst_standard_rate": "nz:statutes/gst/rate#gst_standard_rate",
    "nz-gst/decision.gst_component_from_exclusive_amount": (
        "nz:statutes/gst/rate#gst_component_from_exclusive_amount"
    ),
    "nz-gst/decision.gst_inclusive_amount_from_exclusive_amount": (
        "nz:statutes/gst/rate#gst_inclusive_amount_from_exclusive_amount"
    ),
    "nz-gst/decision.gst_component_from_inclusive_amount": (
        "nz:statutes/gst/rate#gst_component_from_inclusive_amount"
    ),
    "nz-gst/decision.gst_exclusive_amount_from_inclusive_amount": (
        "nz:statutes/gst/rate#gst_exclusive_amount_from_inclusive_amount"
    ),
    "nz-gst/decision.gst_low_value_imported_goods_threshold": (
        "nz:statutes/gst/rate#gst_low_value_imported_goods_threshold"
    ),
    "nz-gst/decision.gst_low_value_imported_goods_subject_to_gst": (
        "nz:statutes/gst/rate#gst_low_value_imported_goods_subject_to_gst"
    ),
    "nz-gst/decision.gst_low_value_imported_goods_component": (
        "nz:statutes/gst/rate#gst_low_value_imported_goods_component"
    ),
    "nz-gst/decision.gst_low_value_imported_goods_total_payable": (
        "nz:statutes/gst/rate#gst_low_value_imported_goods_total_payable"
    ),
}


RULESPEC_NZ_ACC_EARNERS_LEVY_OUTPUTS = {
    "nz-acc/decision.acc_earners_levy_rate_excluding_gst": (
        "nz:regulations/acc/earners_levy#acc_earners_levy_rate_excluding_gst"
    ),
    "nz-acc/decision.acc_earners_levy_rate_including_gst": (
        "nz:regulations/acc/earners_levy#acc_earners_levy_rate_including_gst"
    ),
    "nz-acc/decision.acc_earners_levy_maximum_earnings": (
        "nz:regulations/acc/earners_levy#acc_earners_levy_maximum_earnings"
    ),
    "nz-acc/decision.acc_levy_cents_rounding_scale": (
        "nz:regulations/acc/earners_levy#acc_levy_cents_rounding_scale"
    ),
    "nz-acc/decision.acc_standard_earners_levy_excluding_gst": (
        "nz:regulations/acc/earners_levy#acc_standard_earners_levy_excluding_gst"
    ),
    "nz-acc/decision.acc_standard_earners_levy_including_gst": (
        "nz:regulations/acc/earners_levy#acc_standard_earners_levy_including_gst"
    ),
    "nz-acc/decision.acc_low_self_employed_minimum_earnings": (
        "nz:regulations/acc/earners_levy#acc_low_self_employed_minimum_earnings"
    ),
    "nz-acc/decision.acc_low_self_employed_minimum_levy_excluding_gst": (
        "nz:regulations/acc/earners_levy#acc_low_self_employed_minimum_levy_excluding_gst"
    ),
    "nz-acc/decision.acc_weekly_compensation_purchase_multiplier": (
        "nz:regulations/acc/earners_levy#acc_weekly_compensation_purchase_multiplier"
    ),
    "nz-acc/decision.acc_weekly_compensation_purchase_levy_excluding_gst": (
        "nz:regulations/acc/earners_levy#acc_weekly_compensation_purchase_levy_excluding_gst"
    ),
    "nz-acc/decision.acc_self_employed_invoice_exempt_amount": (
        "nz:regulations/acc/earners_levy#acc_self_employed_invoice_exempt_amount"
    ),
    "nz-acc/decision.acc_self_employed_invoice_levy_payable_after_exempt_amount": (
        "nz:regulations/acc/earners_levy#acc_self_employed_invoice_levy_payable_after_exempt_amount"
    ),
}


RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_OUTPUTS = {
    "nz-income-tax/decision.individual_income_tax_bracket_thresholds": (
        "nz:statutes/income_tax/schedule_1/individual_income_tax#individual_income_tax_bracket_thresholds"
    ),
    "nz-income-tax/decision.individual_income_tax_bracket_rates": (
        "nz:statutes/income_tax/schedule_1/individual_income_tax#individual_income_tax_bracket_rates"
    ),
    "nz-income-tax/decision.individual_income_tax_before_credits": (
        "nz:statutes/income_tax/schedule_1/individual_income_tax#individual_income_tax_before_credits"
    ),
}


class AxiomRuleSpecAdapter:
    """Translate PIC fixture cases to Axiom compiled-execution requests."""

    def __init__(
        self,
        *,
        target: RuleSpecTarget,
        input_id_map: dict[str, str],
        output_id_map: dict[str, str],
        entity: str,
        entity_id: str,
    ) -> None:
        self.target = target
        self.input_id_map = input_id_map
        self.output_id_map = output_id_map
        self.output_id_reverse_map = {axiom_id: pic_id for pic_id, axiom_id in output_id_map.items()}
        self.entity = entity
        self.entity_id = entity_id

    def build_compiled_request(self, pic_case: dict[str, Any]) -> dict[str, Any]:
        period = _period(pic_case["period"])
        interval = {"start": period["start"], "end": period["end"]}
        inputs = [
            {
                "name": self._map_input_id(pic_id),
                "entity": self.entity,
                "entity_id": self.entity_id,
                "interval": interval,
                "value": _scalar_value(value_object["value"]),
            }
            for pic_id, value_object in pic_case.get("inputs", {}).items()
        ]
        outputs = [self._map_output_id(pic_id) for pic_id in pic_case.get("expected", {})]
        return {
            "mode": "explain",
            "dataset": {
                "inputs": inputs,
                "relations": [],
            },
            "queries": [
                {
                    "entity_id": self.entity_id,
                    "period": period,
                    "outputs": outputs,
                }
            ],
        }

    def normalize_response(self, response: dict[str, Any]) -> dict[str, Any]:
        outputs: dict[str, dict[str, Any]] = {}
        traces: dict[str, Any] = {}
        for result in response.get("results", []):
            for axiom_id, output in result.get("outputs", {}).items():
                pic_id = self.output_id_reverse_map.get(axiom_id)
                if pic_id is None:
                    continue
                outputs[pic_id] = _pic_value(output)
            for axiom_id, trace in result.get("trace", {}).items():
                pic_id = self.output_id_reverse_map.get(axiom_id, axiom_id)
                traces[pic_id] = trace
        normalized = {"outputs": outputs}
        if traces:
            normalized["trace"] = traces
        return normalized

    def compare_outputs(
        self,
        *,
        expected: dict[str, Any],
        actual: dict[str, Any],
    ) -> list[str]:
        mismatches: list[str] = []
        for pic_id, expected_value in expected.items():
            actual_value = actual.get(pic_id)
            if actual_value is None:
                mismatches.append(f"{pic_id}: expected {_display(expected_value)}, got missing")
                continue
            if not _values_equal(expected_value, actual_value):
                mismatches.append(
                    f"{pic_id}: expected {_display(expected_value)}, got {_display(actual_value)}"
                )
        return mismatches

    def _map_input_id(self, pic_id: str) -> str:
        try:
            return self.input_id_map[pic_id]
        except KeyError as exc:
            raise KeyError(f"no Axiom input mapping for PIC id: {pic_id}") from exc

    def _map_output_id(self, pic_id: str) -> str:
        try:
            return self.output_id_map[pic_id]
        except KeyError as exc:
            raise KeyError(f"no Axiom output mapping for PIC id: {pic_id}") from exc


def build_rulespec_nz_gst_adapter() -> AxiomRuleSpecAdapter:
    return AxiomRuleSpecAdapter(
        target=RULESPEC_NZ_GST_TARGET,
        input_id_map=RULESPEC_NZ_GST_INPUTS,
        output_id_map=RULESPEC_NZ_GST_OUTPUTS,
        entity="Supply",
        entity_id="supply:1",
    )


def build_rulespec_nz_acc_earners_levy_adapter() -> AxiomRuleSpecAdapter:
    return AxiomRuleSpecAdapter(
        target=RULESPEC_NZ_ACC_EARNERS_LEVY_TARGET,
        input_id_map=RULESPEC_NZ_ACC_EARNERS_LEVY_INPUTS,
        output_id_map=RULESPEC_NZ_ACC_EARNERS_LEVY_OUTPUTS,
        entity="Person",
        entity_id="person:1",
    )


def build_rulespec_nz_individual_income_tax_adapter() -> AxiomRuleSpecAdapter:
    return AxiomRuleSpecAdapter(
        target=RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_TARGET,
        input_id_map=RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_INPUTS,
        output_id_map=RULESPEC_NZ_INDIVIDUAL_INCOME_TAX_OUTPUTS,
        entity="Person",
        entity_id="person:1",
    )


def _period(period: str) -> dict[str, str]:
    if "/" in period:
        start, end = period.split("/", maxsplit=1)
        if _is_date(start) and _is_date(end):
            return {
                "period_kind": "tax_year",
                "start": start,
                "end": end,
            }
        raise ValueError(f"unsupported PIC date range for Axiom request: {period}")
    if _is_date(period):
        return {
            "period_kind": "custom",
            "name": "calendar_day",
            "start": period,
            "end": period,
        }
    if len(period) == 7 and period[4] == "-":
        year = int(period[:4])
        month = int(period[5:])
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)
        return {
            "period_kind": "month",
            "start": start.isoformat(),
            "end": end.isoformat(),
        }
    if len(period) == 4 and period.isdigit():
        return {
            "period_kind": "year",
            "start": f"{period}-01-01",
            "end": f"{int(period) + 1}-01-01",
        }
    raise ValueError(f"unsupported PIC period for Axiom request: {period}")


def _is_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return len(value) == 10


def _scalar_value(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        return {"kind": "bool", "value": value}
    if isinstance(value, int):
        return {"kind": "integer", "value": value}
    if isinstance(value, str):
        if _is_decimal_string(value):
            return {"kind": "decimal", "value": value}
        if _is_date(value):
            return {"kind": "date", "value": value}
        return {"kind": "text", "value": value}
    raise TypeError(f"unsupported PIC value for Axiom request: {value!r}")


def _pic_value(output: dict[str, Any]) -> dict[str, Any]:
    if output.get("kind") == "judgment":
        return {
            "value": output.get("outcome"),
            "valueState": "known",
        }
    scalar = output.get("value", {})
    value = scalar.get("value")
    value_object: dict[str, Any] = {
        "value": value,
        "valueState": "known",
    }
    if output.get("unit") in {"NZD", "USD", "AUD", "GBP", "EUR"}:
        value_object["currency"] = output["unit"]
    return value_object


def _values_equal(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    if expected.get("valueState") != actual.get("valueState"):
        return False
    if expected.get("currency") != actual.get("currency"):
        return False
    expected_value = expected.get("value")
    actual_value = actual.get("value")
    if _is_decimalish(expected_value) and _is_decimalish(actual_value):
        return Decimal(str(expected_value)) == Decimal(str(actual_value))
    return expected_value == actual_value


def _is_decimalish(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, str):
        return _is_decimal_string(value)
    return False


def _is_decimal_string(value: str) -> bool:
    try:
        Decimal(value)
    except InvalidOperation:
        return False
    return True


def _display(value_object: dict[str, Any]) -> str:
    return str(value_object.get("value"))
