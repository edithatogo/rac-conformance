import json
import sys
from pathlib import Path
from unittest.mock import patch

from pic_contracts.validate_examples import main


def _write(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def test_main_with_valid_corpus(tmp_path: Path, capsys) -> None:
    example_root = tmp_path / "pic-crosswalk" / "0.1.0" / "examples"
    valid_path = example_root / "valid" / "example.json"

    doc = {"valueState": "known"}
    _write(valid_path, doc)

    assert main([str(tmp_path)]) == 0

    captured = capsys.readouterr()
    assert "OK: example corpus under" in captured.out


def test_main_with_invalid_corpus_reports_issues(tmp_path: Path, capsys) -> None:
    example_root = tmp_path / "pic-crosswalk" / "0.1.0" / "examples"
    valid_path = example_root / "valid" / "bad.json"

    doc = {"conformsTo": "pic-crosswalk/0.1.0", "wrong": "format"}
    _write(valid_path, doc)

    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert "schema:" in captured.out
    assert str(valid_path) in captured.out


def test_main_with_unexpectedly_valid_corpus_reports_issues(tmp_path: Path, capsys) -> None:
    example_root = tmp_path / "pic-crosswalk" / "0.1.0" / "examples"
    invalid_path = example_root / "invalid" / "unexpectedly_valid.json"

    doc = {"valueState": "known"}
    _write(invalid_path, doc)

    assert main([str(tmp_path)]) == 1

    captured = capsys.readouterr()
    assert "negative-test:" in captured.out
    assert str(invalid_path) in captured.out
    assert "invalid example unexpectedly passed validation" in captured.out


def test_main_without_argv_uses_sys_argv(tmp_path: Path, capsys) -> None:
    with patch.object(sys, "argv", ["pic-validate-examples", str(tmp_path)]):
        assert main() == 0

        captured = capsys.readouterr()
        assert f"OK: example corpus under {tmp_path}" in captured.out


def test_main_with_expected_invalid_corpus(tmp_path: Path, capsys) -> None:
    example_root = tmp_path / "pic-crosswalk" / "0.1.0" / "examples"
    invalid_path = example_root / "invalid" / "expected_invalid.json"

    doc = {"conformsTo": "pic-crosswalk/0.1.0", "wrong": "format"}
    _write(invalid_path, doc)

    assert main([str(tmp_path)]) == 0

    captured = capsys.readouterr()
    assert "OK: example corpus under" in captured.out
