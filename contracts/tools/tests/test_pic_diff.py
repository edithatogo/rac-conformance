import json
from copy import deepcopy

import pytest

from pic_contracts.diff import changes_to_markdown, diff_files, diff_parameters
from pic_contracts.safety import SafetyLimitError


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
    assert [change.kind for change in changes] == ["removed_period", "new_period", "new_period"]


def test_diff_reports_removed_parameter() -> None:
    before = _doc()
    after = {"conformsTo": "pic-parameters/0.1.0", "parameters": []}
    changes = diff_parameters(before, after)
    assert [change.kind for change in changes] == ["removed_parameter"]


def test_diff_files(tmp_path) -> None:
    before_file = tmp_path / "before.json"
    after_file = tmp_path / "after.json"

    before_file.write_text(json.dumps(_doc(20)))
    after_file.write_text(json.dumps(_doc(21)))

    changes = diff_files(before_file, after_file)
    assert [change.kind for change in changes] == ["value_change"]
    assert "20 -> 21" in changes[0].detail

def test_diff_files_file_not_found(tmp_path) -> None:
    before_file = tmp_path / "before.json"
    after_file = tmp_path / "after.json"

    before_file.write_text(json.dumps(_doc(20)))

    with pytest.raises(FileNotFoundError):
        diff_files(before_file, after_file)

def test_diff_files_malformed_json(tmp_path) -> None:
    before_file = tmp_path / "before.json"
    after_file = tmp_path / "after.json"

    before_file.write_text(json.dumps(_doc(20)))
    after_file.write_text("invalid json")

    with pytest.raises(json.JSONDecodeError):
        diff_files(before_file, after_file)

def test_diff_files_not_dict_safety_limit(tmp_path) -> None:
    before_file = tmp_path / "before.json"
    after_file = tmp_path / "after.json"

    before_file.write_text(json.dumps(_doc(20)))
    after_file.write_text(json.dumps([]))

    with pytest.raises(SafetyLimitError):
        diff_files(before_file, after_file)
