import json
from pathlib import Path

from pic_contracts.diff_cli import main as diff_main
from pic_contracts.validate_cli import main as validate_main
from pic_contracts.validate_examples import main as examples_main
from pic_contracts.validation import validate_path


def _write(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def _parameters(value: int = 20) -> dict:
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


def test_diff_cli_markdown_and_json(tmp_path: Path, capsys) -> None:
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    _write(before, _parameters(20))
    _write(after, _parameters(21))
    assert diff_main([str(before), str(after)]) == 0
    assert "value_change" in capsys.readouterr().out

    assert diff_main([str(before), str(after), "--json"]) == 0
    assert '"kind": "value_change"' in capsys.readouterr().out


def test_validate_cli_human_and_json_output(tmp_path: Path, capsys) -> None:
    path = tmp_path / "params.json"
    _write(path, _parameters())
    assert validate_main([str(path)]) == 0
    assert "OK:" in capsys.readouterr().out

    bad = tmp_path / "bad.json"
    bad.write_text("[1, 2, 3]", encoding="utf-8")
    assert validate_main([str(bad), "--json"]) == 1
    assert '"ok": false' in capsys.readouterr().out


def test_validate_examples_main_passes_repo_corpus(capsys) -> None:
    assert examples_main(["../../contracts"]) == 0
    assert "OK:" in capsys.readouterr().out


def test_validate_examples_main_reports_invalid_positive(tmp_path: Path, capsys) -> None:
    invalid = tmp_path / "pic-test" / "0.1.0" / "examples" / "invalid" / "unexpected.json"
    _write(invalid, {"valueState": "known"})
    assert examples_main([str(tmp_path)]) == 1
    assert "unexpectedly passed" in capsys.readouterr().out


def test_validate_path_reports_no_json_files(tmp_path: Path) -> None:
    report = validate_path(tmp_path)
    assert not report.ok
    assert report.issues[0].code == "input"

