from __future__ import annotations

from snap_divergence.policyengine_runner import load_cases
from snap_divergence.prd_runner import build_prd_row, format_prd_result


def test_build_prd_row_uses_fixed_person_slots_and_annual_values() -> None:
    case = load_cases(
        "studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json",
        case_ids=["us-snap/fixture.tx_baseline_family_low_income"],
    )[0]

    row = build_prd_row(case)

    assert row["ruleYear"] == 2026
    assert row["stateFIPS"] == 48
    assert row["famsize"] == 4
    assert row["income"] == 21600.0
    assert row["netexp.childcare"] == 3000.0
    assert row["netexp.rentormortgage"] == 15600.0
    assert row["netexp.utilities"] == 3000.0
    assert row["agePerson1"] == 35
    assert row["agePerson4"] == 5
    assert row["agePerson5"] is None


def test_build_prd_row_marks_disability_for_elderly_disabled_pair() -> None:
    case = load_cases(
        "studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json",
        case_ids=["us-snap/fixture.ms_elderly_medical_uncapped_shelter"],
    )[0]

    row = build_prd_row(case)

    assert row["agePerson1"] == 67
    assert row["disability2"] == 1
    assert row["oop.add_for_elderlyordisabled"] == 4200.0


def test_format_prd_result_normalizes_annual_snap_value_to_monthly() -> None:
    result = format_prd_result("us-snap/fixture.example", "2026-01", annual_snap_value=1200)

    assert result["outputs"]["us-snap/decision.eligible"] == {
        "value": True,
        "valueState": "known",
    }
    assert result["outputs"]["us-snap/decision.allotment"] == {
        "value": "100",
        "valueState": "known",
        "currency": "USD",
        "tolerance": "1.00",
    }
    assert result["rawOutputs"]["snapValueAnnual"] == "1200"
