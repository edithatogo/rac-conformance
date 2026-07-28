from datetime import date
from pathlib import Path

import pytest

from pic_contracts.parameters import _parse_date, validate_parameter_periods
from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json, validator_for

BASE = CONTRACTS_ROOT / "pic-parameters" / "0.1.0" / "examples"


def test_valid_parameters_validate_and_have_consistent_periods() -> None:
    validator = validator_for("pic-parameters")
    for path in sorted((BASE / "valid").glob("*.json")):
        doc = load_json(path)
        validator.validate(doc)
        assert validate_parameter_periods(doc) == []


def test_decimal_string_parameter_value_is_accepted() -> None:
    validator = validator_for("pic-parameters")
    doc = load_json(BASE / "valid" / "threshold.json")
    doc["parameters"][0]["values"][0]["value"] = "20.00"
    validator.validate(doc)


def test_schema_rejects_float_value() -> None:
    validator = validator_for("pic-parameters")
    errors = list(validator.iter_errors(load_json(BASE / "invalid" / "float-value.json")))
    assert errors
    assert any(
        Path(*map(str, error.path)) == Path("parameters/0/values/0/value")
        for error in errors
    )


def test_period_validator_rejects_overlapping_periods() -> None:
    doc = load_json(BASE / "invalid" / "overlapping-periods.json")
    errors = validate_parameter_periods(doc)
    assert errors
    assert errors[0].path == "parameters/0/values/1"
    assert "overlaps" in errors[0].message


def test_period_validator_rejects_unordered_after_open_ended_period() -> None:
    doc = load_json(BASE / "invalid" / "unordered-periods.json")
    errors = validate_parameter_periods(doc)
    assert errors
    assert errors[0].path == "parameters/0/values/1"
    assert "open-ended" in errors[0].message




def test_parse_date_with_none() -> None:
    assert _parse_date(None) is None

def test_parse_date_with_valid_string() -> None:
    assert _parse_date("2023-10-27") == date(2023, 10, 27)

def test_parse_date_with_invalid_string() -> None:
    with pytest.raises(ValueError):
        _parse_date("invalid-date")

    with pytest.raises(ValueError):
        _parse_date("2023/10/27")

    with pytest.raises(ValueError):
        _parse_date("2023-13-40")
