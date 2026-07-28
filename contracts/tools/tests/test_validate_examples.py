import json
from pathlib import Path

from pic_contracts.validate_examples import main, validate_example_corpus


def _write(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def _valid_doc() -> dict:
    return {"valueState": "known"}


def _invalid_doc() -> dict:
    return {"conformsTo": "pic-traces/0.1.0"}  # Missing required fields


def test_validate_example_corpus_success(tmp_path: Path) -> None:
    _write(tmp_path / "pic-foo/bar/examples/valid/test1.json", _valid_doc())
    _write(tmp_path / "process-profile/baz/examples/invalid/test2.json", _invalid_doc())

    report = validate_example_corpus(tmp_path)

    assert report.ok
    assert len(report.issues) == 0


def test_validate_example_corpus_valid_file_fails(tmp_path: Path) -> None:
    _write(tmp_path / "pic-foo/bar/examples/valid/test1.json", _invalid_doc())

    report = validate_example_corpus(tmp_path)

    assert not report.ok
    assert len(report.issues) > 0
    assert any("is a required property" in issue.message for issue in report.issues)


def test_validate_example_corpus_invalid_file_passes(tmp_path: Path) -> None:
    invalid_path = tmp_path / "pic-foo/bar/examples/invalid/test1.json"
    _write(invalid_path, _valid_doc())

    report = validate_example_corpus(tmp_path)

    assert not report.ok
    assert len(report.issues) == 1
    issue = report.issues[0]
    assert issue.code == "negative-test"
    assert issue.message == "invalid example unexpectedly passed validation"
    assert issue.path == str(invalid_path)


def test_main_success(tmp_path: Path, capsys) -> None:
    _write(tmp_path / "pic-foo/bar/examples/valid/test1.json", _valid_doc())

    result = main([str(tmp_path)])

    assert result == 0
    captured = capsys.readouterr()
    assert "OK: example corpus under" in captured.out


def test_main_failure(tmp_path: Path, capsys) -> None:
    _write(tmp_path / "pic-foo/bar/examples/valid/test1.json", _invalid_doc())

    result = main([str(tmp_path)])

    assert result == 1
    captured = capsys.readouterr()
    assert "schema:" in captured.out
