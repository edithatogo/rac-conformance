from copy import deepcopy

from pic_contracts.diff import _period_key, changes_to_markdown, diff_parameters


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


def test_period_key_both_present() -> None:
    assert _period_key({"from": "2026-01-01", "to": "2026-12-31"}) == ("2026-01-01", "2026-12-31")

def test_period_key_only_from_present() -> None:
    assert _period_key({"from": "2026-01-01"}) == ("2026-01-01", None)

def test_period_key_only_to_present() -> None:
    assert _period_key({"to": "2026-12-31"}) == ("", "2026-12-31")

def test_period_key_neither_present() -> None:
    assert _period_key({}) == ("", None)

def test_period_key_to_is_none() -> None:
    assert _period_key({"from": "2026-01-01", "to": None}) == ("2026-01-01", None)
