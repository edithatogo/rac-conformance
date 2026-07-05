from __future__ import annotations

from decimal import Decimal

import pytest

from snap_divergence.policyengine_runner import (
    PolicyEngineUnavailable,
    build_policyengine_situation,
    format_run_result,
    load_cases,
    monthly_money,
    write_results,
)


def test_load_cases_filters_by_case_id() -> None:
    cases = load_cases(
        "studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json",
        case_ids=["us-snap/fixture.tx_asset_above_limit"],
    )

    assert [case["caseId"] for case in cases] == ["us-snap/fixture.tx_asset_above_limit"]


def test_build_policyengine_situation_annualizes_monthly_values() -> None:
    case = load_cases(
        "studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json",
        case_ids=["us-snap/fixture.ca_baseline_family_low_income"],
    )[0]

    situation = build_policyengine_situation(case)
    members = situation["spm_units"]["spm_unit"]["members"]

    assert members == ["head", "spouse", "child1", "child2"]
    assert situation["people"]["head"]["employment_income"] == {"2026": 21600.0}
    assert situation["households"]["household"]["state_code_str"] == "CA"
    assert situation["spm_units"]["spm_unit"]["housing_cost"] == {"2026": 15600.0}
    assert situation["spm_units"]["spm_unit"]["snap_assets"] == {"2026": 500.0}


def test_build_policyengine_situation_marks_elderly_disabled_member() -> None:
    case = load_cases(
        "studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json",
        case_ids=["us-snap/fixture.pa_elderly_medical_uncapped_shelter"],
    )[0]

    situation = build_policyengine_situation(case)

    assert situation["people"]["head"]["age"] == {"2026": 67}
    assert situation["people"]["spouse"]["is_disabled"] == {"2026": True}
    assert situation["people"]["head"]["snap_allowable_medical_expenses"] == {
        "2026": 4200.0,
    }


def test_monthly_money_rejects_missing_value() -> None:
    with pytest.raises(ValueError, match="money input missing value"):
        monthly_money({"valueState": "unknown"}, "us-snap/variable.earned_income_monthly")


def test_format_run_result_uses_pic_value_objects() -> None:
    result = format_run_result(
        case_id="us-snap/fixture.example",
        period="2026-01",
        eligible=True,
        allotment=Decimal("291.25"),
        trace=None,
    )

    assert result["caseId"] == "us-snap/fixture.example"
    assert result["outputs"]["us-snap/decision.eligible"] == {
        "value": True,
        "valueState": "known",
    }
    assert result["outputs"]["us-snap/decision.allotment"] == {
        "value": "291.25",
        "valueState": "known",
        "currency": "USD",
        "tolerance": "1.00",
    }


def test_write_results_uses_jsonl_when_requested(tmp_path) -> None:
    path = tmp_path / "results.jsonl"

    write_results(path, [{"caseId": "a"}, {"caseId": "b"}])

    assert path.read_text().splitlines() == ['{"caseId": "a"}', '{"caseId": "b"}']


def test_policyengine_unavailable_error_is_explicit(monkeypatch: pytest.MonkeyPatch) -> None:
    import snap_divergence.policyengine_runner as runner

    monkeypatch.setattr(runner, "_load_policyengine_simulation", lambda: None)

    with pytest.raises(PolicyEngineUnavailable, match=".venv-policyengine"):
        runner.run_policyengine_case({"caseId": "us-snap/fixture.empty", "period": "2026-01"})
