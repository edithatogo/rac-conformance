import json
from pathlib import Path

import pytest

from pic_contracts.safety import SafetyLimitError, load_bounded_json


def test_bounded_loader_accepts_small_object(tmp_path: Path) -> None:
    path = tmp_path / "input.json"
    path.write_text(json.dumps({"ok": [1, 2]}), encoding="utf-8")
    assert load_bounded_json(path) == {"ok": [1, 2]}


def test_bounded_loader_rejects_oversized_input(tmp_path: Path) -> None:
    path = tmp_path / "input.json"
    path.write_text(json.dumps({"value": "x" * 20}), encoding="utf-8")
    with pytest.raises(SafetyLimitError, match="max_bytes"):
        load_bounded_json(path, max_bytes=10)


def test_bounded_loader_rejects_deep_input(tmp_path: Path) -> None:
    value = "leaf"
    for _ in range(8):
        value = {"nested": value}
    path = tmp_path / "input.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(SafetyLimitError, match="max_depth"):
        load_bounded_json(path, max_depth=3)


def test_bounded_loader_rejects_large_string(tmp_path: Path) -> None:
    path = tmp_path / "input.json"
    path.write_text(json.dumps({"value": "x" * 20}), encoding="utf-8")
    with pytest.raises(SafetyLimitError, match="max_string_bytes"):
        load_bounded_json(path, max_string_bytes=10)
