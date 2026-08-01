import json
from pathlib import Path

import pytest

from pic_contracts.diff_cli import main


def _write(path: Path, doc: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


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


def test_diff_cli_markdown(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    before = _write(tmp_path / "before.json", _doc(20))
    after = _write(tmp_path / "after.json", _doc(21))

    result = main([str(before), str(after)])
    assert result == 0

    out, _err = capsys.readouterr()
    assert "nz-oia/parameter.limit" in out
    assert "20 -> 21" in out
    assert "value_change" in out


def test_diff_cli_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    before = _write(tmp_path / "before.json", _doc(20))
    after = _write(tmp_path / "after.json", _doc(21))

    result = main([str(before), str(after), "--json"])
    assert result == 0

    out, _err = capsys.readouterr()
    # verify valid JSON output
    data = json.loads(out)
    assert len(data) == 1
    assert data[0]["kind"] == "value_change"
    assert data[0]["parameter_id"] == "nz-oia/parameter.limit"
    assert "20 -> 21" in data[0]["detail"]


def test_diff_cli_missing_file_raises_systemexit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    before = _write(tmp_path / "before.json", _doc(20))
    after = tmp_path / "does_not_exist.json"

    with pytest.raises(SystemExit) as exc_info:
        main([str(before), str(after)])

    # argparse error calls sys.exit(2)
    assert exc_info.value.code == 2

    _out, err = capsys.readouterr()
    assert "does not exist" in err
    assert "does_not_exist.json" in err


def test_diff_cli_missing_arguments_raises_systemexit(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([])

    assert exc_info.value.code == 2

    _out, err = capsys.readouterr()
    assert "the following arguments are required" in err or "too few arguments" in err
