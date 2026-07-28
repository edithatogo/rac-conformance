from copy import deepcopy

import pytest

from pic_contracts.diff import _parameters_by_id, changes_to_markdown, diff_parameters


def _doc(value: int = 20) -> dict:
    return {
        "conformsTo": "pic-parameters/0.1.0",
        "parameters": [
            {
                "id": "nz-oia/parameter.limit",
                "label": "Limit",
                "unit": "working_days",
                "calendar": {"timezone": "Pacific/Auckland", "convention": "test"},
                "values": [
                    {
                        "from": "2026-01-01",
                        "to": None,
                        "value": value,
                        "sourceRefs": ["test"],
                    }
                ],
            }
        ],
    }


def test_diff_reports_unchanged() -> None:
    assert diff_parameters(_doc(), _doc()) == []
    assert "No changes" in changes_to_markdown([])


def test_diff_reports_value_change() -> None:
    changes = diff_parameters(_doc(20), _doc(21))
    assert [change.kind for change in changes] == ["value_change"]
    assert "20 -> 21" in changes[0].detail


def test_diff_reports_new_period() -> None:
    before = _doc()
    after = deepcopy(before)
    after["parameters"][0]["values"].append(
        {"from": "2027-01-01", "to": None, "value": 21, "sourceRefs": ["test"]}
    )
    after["parameters"][0]["values"][0]["to"] = "2027-01-01"
    changes = diff_parameters(before, after)
    assert [change.kind for change in changes] == [
        "removed_period",
        "new_period",
        "new_period",
    ]


def test_diff_reports_removed_parameter() -> None:
    before = _doc()
    after = {"conformsTo": "pic-parameters/0.1.0", "parameters": []}
    changes = diff_parameters(before, after)
    assert [change.kind for change in changes] == ["removed_parameter"]


def test_parameters_by_id_happy_path() -> None:
    doc = {
        "parameters": [
            {"id": "param1", "value": 1},
            {"id": "param2", "value": 2},
        ]
    }
    result = _parameters_by_id(doc)
    assert result == {
        "param1": {"id": "param1", "value": 1},
        "param2": {"id": "param2", "value": 2},
    }


def test_parameters_by_id_missing_parameters_key() -> None:
    doc = {"other_key": "value"}
    assert _parameters_by_id(doc) == {}


def test_parameters_by_id_empty_parameters_list() -> None:
    doc = {"parameters": []}
    assert _parameters_by_id(doc) == {}


def test_parameters_by_id_missing_id_key() -> None:
    doc = {
        "parameters": [
            {"not_id": "param1", "value": 1},
        ]
    }
    with pytest.raises(KeyError):
        _parameters_by_id(doc)
