from __future__ import annotations

from nz_reconciliation.mapping import annotate_inventory_case, openfisca_mapping_for_case
from nz_reconciliation.pic_cases import inventory_case_to_pic_case


def test_openfisca_mapping_marks_income_tax_engine_gap() -> None:
    mapping = openfisca_mapping_for_case({"domain": "income_tax"})
    assert mapping["status"] == "engine_gap"
    assert mapping["classification"] == "engine_gap"


def test_annotate_inventory_case_updates_openfisca_block() -> None:
    case = {
        "caseId": "nz-recon/income_tax.x",
        "domain": "income_tax",
        "openfiscaAotearoa": {
            "repo": "ServiceInnovationLab/openfisca-aotearoa",
            "status": "pending_mapping",
        },
    }
    annotated = annotate_inventory_case(case)
    assert annotated["openfiscaAotearoa"]["status"] == "engine_gap"
    assert (
        "progressive" in annotated["openfiscaAotearoa"]["notes"].lower()
        or "tax" in annotated["openfiscaAotearoa"]["notes"].lower()
    )


def test_inventory_case_to_pic_case_maps_income_tax_ids() -> None:
    case = {
        "caseId": "nz-recon/income_tax.first_bracket_upper_bound",
        "name": "first_bracket_upper_bound",
        "domain": "income_tax",
        "period": "2026-04-01/2027-03-31",
        "inputs": {
            "nz:statutes/income_tax/schedule_1/individual_income_tax#input.taxable_income": 15600,
        },
        "expectedRulespec": {
            "nz:statutes/income_tax/schedule_1/individual_income_tax#individual_income_tax_bracket_thresholds": 15600,
            "nz:statutes/income_tax/schedule_1/individual_income_tax#individual_income_tax_before_credits": 1638,
        },
        "sourceRefs": ["https://example.test"],
        "rulespec": {
            "testPath": "nz/statutes/income_tax/schedule_1/individual_income_tax.test.yaml"
        },
    }
    pic = inventory_case_to_pic_case(case)
    assert "nz-income-tax/variable.taxable_income" in pic["inputs"]
    assert pic["inputs"]["nz-income-tax/variable.taxable_income"]["value"] == "15600"
    assert "nz-income-tax/decision.individual_income_tax_before_credits" in pic["expected"]
    assert "nz-income-tax/decision.individual_income_tax_bracket_thresholds" not in pic["expected"]
    assert (
        pic["expected"]["nz-income-tax/decision.individual_income_tax_before_credits"]["value"]
        == "1638"
    )
