from __future__ import annotations

import pytest

from pic_fixture_converters import (
    UnsupportedConstructError,
    pic_to_policyengine,
    policyengine_to_pic,
)


def test_policyengine_minimal_round_trip() -> None:
    source = {
        "name": "Vermont EITC",
        "period": "2026",
        "input": {"state_code": "VT", "eitc": 1000, "tax_unit_child_dependents": 1},
        "output": {"vt_eitc": 380},
        "absolute_error_margin": 0,
    }

    fixture = policyengine_to_pic(source)[0]
    case = fixture["cases"][0]

    assert case["inputs"]["native/policyengine/state_code.value"]["value"] == "VT"
    assert case["expected"]["native/policyengine/vt_eitc.value"]["value"] == 380
    assert pic_to_policyengine(fixture) == [source]


def test_policyengine_multi_entity_round_trip() -> None:
    source = {
        "name": "SPM unit",
        "period": "2026",
        "input": {
            "people": {
                "person1": {"age": 40, "employment_income": {"2026": 10_000}},
                "person2": {"age": 12},
            },
            "spm_units": {"unit1": {"snap": 100}},
        },
        "output": {"people": {"person1": {"taxable_income": 9_000}}},
    }

    fixture = policyengine_to_pic(source)[0]

    assert pic_to_policyengine(fixture) == [source]


def test_policyengine_rejects_dotted_input_keys_as_parameter_reforms() -> None:
    with pytest.raises(UnsupportedConstructError, match="dotted_input_key"):
        policyengine_to_pic(
            {
                "name": "Inline reform",
                "period": "2026",
                "input": {"gov.contrib.example.parameter": True, "salary": 1},
                "output": {"tax": 0},
            }
        )


def test_policyengine_rejects_margin_mapping() -> None:
    with pytest.raises(UnsupportedConstructError, match="absolute_error_margin_mapping"):
        policyengine_to_pic(
            {
                "name": "Margin mapping",
                "period": "2026",
                "input": {"salary": 1},
                "output": {"tax": 0},
                "absolute_error_margin": {"tax": 0.01},
            }
        )


def test_policyengine_rejects_unexpected_fields() -> None:
    with pytest.raises(UnsupportedConstructError, match="unexpected_field"):
        policyengine_to_pic(
            {
                "name": "Unexpected",
                "period": "2026",
                "input": {"salary": 1},
                "output": {"tax": 0},
                "max_spiral_loops": 4,
            }
        )
