from __future__ import annotations

import json
from pathlib import Path

from tools.validate_project14_allowlist import main


def test_allowlist_accepts_required_items(tmp_path: Path, monkeypatch) -> None:
    items = {
        "items": [
            {"content": {"repository": "edithatogo/foi-o", "number": 23}, "status": "Todo"},
            {"content": {"repository": "edithatogo/rac-conformance", "number": 30}, "status": "Todo"},
        ]
    }
    allowlist = {
                "project": 14,
                "expected_status": "Todo",
                "required_items": ["edithatogo/foi-o#23", "edithatogo/rac-conformance#30"],
        "allowed_repositories": ["edithatogo/foi-o", "edithatogo/rac-conformance"],
    }
    items_path = tmp_path / "items.json"
    allowlist_path = tmp_path / "allowlist.json"
    items_path.write_text(json.dumps(items), encoding="utf-8")
    allowlist_path.write_text(json.dumps(allowlist), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["check", "--items", str(items_path), "--allowlist", str(allowlist_path)])

    assert main() == 0


def test_allowlist_reports_missing_and_unrelated_items(tmp_path: Path, monkeypatch) -> None:
    items_path = tmp_path / "items.json"
    allowlist_path = tmp_path / "allowlist.json"
    items_path.write_text(
        json.dumps({"items": [{"content": {"repository": "example/other", "number": 1}}]}),
        encoding="utf-8",
    )
    allowlist_path.write_text(
        json.dumps(
            {
                "project": 14,
                "expected_status": "Todo",
                "required_items": ["edithatogo/foi-o#23"],
                "allowed_repositories": ["edithatogo/foi-o"],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["check", "--items", str(items_path), "--allowlist", str(allowlist_path)])

    assert main() == 1


def test_allowlist_reports_stale_required_status(tmp_path: Path, monkeypatch) -> None:
    items_path = tmp_path / "items.json"
    allowlist_path = tmp_path / "allowlist.json"
    items_path.write_text(
        json.dumps(
            {"items": [{"content": {"repository": "edithatogo/foi-o", "number": 23}, "status": "Done"}]}
        ),
        encoding="utf-8",
    )
    allowlist_path.write_text(
        json.dumps(
            {
                "project": 14,
                "expected_status": "Todo",
                "required_items": ["edithatogo/foi-o#23"],
                "allowed_repositories": ["edithatogo/foi-o"],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["check", "--items", str(items_path), "--allowlist", str(allowlist_path)])

    assert main() == 1


def test_allowlist_reports_extra_item_in_allowed_repository(tmp_path: Path, monkeypatch) -> None:
    items_path = tmp_path / "items.json"
    allowlist_path = tmp_path / "allowlist.json"
    items_path.write_text(
        json.dumps(
            {
                "items": [
                    {"content": {"repository": "edithatogo/foi-o", "number": 23}},
                    {"content": {"repository": "edithatogo/foi-o", "number": 99}},
                ]
            }
        ),
        encoding="utf-8",
    )
    allowlist_path.write_text(
        json.dumps(
            {
                "project": 14,
                "required_items": ["edithatogo/foi-o#23"],
                "allowed_repositories": ["edithatogo/foi-o"],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["check", "--items", str(items_path), "--allowlist", str(allowlist_path)])

    assert main() == 1
