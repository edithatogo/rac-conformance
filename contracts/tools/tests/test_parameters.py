import pytest
from datetime import date

from pic_contracts.parameters import _parse_date


def test_parse_date_with_none():
    assert _parse_date(None) is None


def test_parse_date_with_valid_iso_string():
    assert _parse_date("2023-10-25") == date(2023, 10, 25)


def test_parse_date_with_invalid_string_raises_value_error():
    with pytest.raises(ValueError):
        _parse_date("invalid-date")


def test_parse_date_with_invalid_type_raises_type_error():
    with pytest.raises(TypeError):
        _parse_date(123)
