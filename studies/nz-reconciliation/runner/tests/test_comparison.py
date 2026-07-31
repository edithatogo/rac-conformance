from __future__ import annotations

from decimal import Decimal

import pytest
from nz_reconciliation.comparison import compare_pair, compare_result_sets


def test_compare_pair_agreement_within_tolerance() -> None:
    rulespec = {
        "caseId": "nz-recon/income_tax.first_bracket_upper_bound",
        "domain": "income_tax",
        "outputs": {"tax": {"value": "1638.00"}},
    }
    openfisca = {
        "caseId": "nz-recon/income_tax.first_bracket_upper_bound",
        "domain": "income_tax",
        "outputs": {"tax": {"value": "1638.00"}},
    }
    row = compare_pair(rulespec, openfisca)
    assert row["agreement"] is True
    assert row["classification"] == "agreement"
    assert row["valueDifference"] == "0"


def test_compare_pair_divergence_outside_tolerance() -> None:
    rulespec = {
        "caseId": "nz-recon/acc.standard_2026_earnings_below_cap",
        "domain": "acc_earners_levy",
        "outputs": {"levy": {"value": "1520"}},
    }
    openfisca = {
        "caseId": "nz-recon/acc.standard_2026_earnings_below_cap",
        "domain": "acc_earners_levy",
        "outputs": {"levy": {"value": "1600"}},
    }
    row = compare_pair(rulespec, openfisca, tolerance=Decimal("0.01"))
    assert row["agreement"] is False
    assert row["valueDifference"] == "80"


def test_compare_result_sets_requires_matching_ids() -> None:
    with pytest.raises(ValueError, match="case id mismatch"):
        compare_result_sets(
            [{"caseId": "a", "outputs": {"x": {"value": "1"}}}],
            [{"caseId": "b", "outputs": {"x": {"value": "1"}}}],
        )


def test_compare_result_sets_orders_by_case_id() -> None:
    rows = compare_result_sets(
        [
            {"caseId": "b", "outputs": {"x": {"value": "2"}}},
            {"caseId": "a", "outputs": {"x": {"value": "1"}}},
        ],
        [
            {"caseId": "a", "outputs": {"x": {"value": "1"}}},
            {"caseId": "b", "outputs": {"x": {"value": "2"}}},
        ],
    )
    assert [row["caseId"] for row in rows] == ["a", "b"]


def test_compare_pair_engine_gap_is_classified_not_numeric() -> None:
    rulespec = {
        "caseId": "nz-recon/income_tax.first_bracket_upper_bound",
        "domain": "income_tax",
        "status": "exact_match",
        "outputs": {"tax": {"value": "1638"}},
    }
    openfisca = {
        "caseId": "nz-recon/income_tax.first_bracket_upper_bound",
        "domain": "income_tax",
        "status": "engine_gap",
        "outputs": {},
        "notes": "no progressive tax formula",
        "evidence": ["openfisca_aotearoa/variables/acts/income_tax/individual.py"],
    }
    row = compare_pair(rulespec, openfisca)
    assert row["agreement"] is False
    assert row["classification"] == "engine_gap"
    assert row["valueDifference"] is None
    assert "openfisca_aotearoa/variables/acts/income_tax/individual.py" in row["evidence"]
