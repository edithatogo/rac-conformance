import json
from pathlib import Path

from pic_contracts.validate_cli import main
from pic_contracts.validation import detect_contract, validate_path


def _write(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def _crosswalk(data_type: str = "money") -> dict:
    return {
        "conformsTo": "pic-crosswalk/0.1.0",
        "jurisdictionScope": {"country": "NZ"},
        "provenance": {"curator": "test", "method": "ai-proposed", "source": "test"},
        "rows": [
            {
                "id": "nz-oia/variable.amount",
                "label": "Amount",
                "kind": "variable",
                "dataType": data_type,
                "mappings": [{"system": "test", "ref": "amount", "method": "ai-proposed"}],
                "sourceRefs": ["test"],
                "definition": "test",
            },
            {
                "id": "nz-oia/parameter.limit",
                "label": "Limit",
                "kind": "parameter",
                "dataType": "integer",
                "mappings": [{"system": "test", "ref": "limit", "method": "ai-proposed"}],
                "sourceRefs": ["test"],
                "definition": "test",
            },
        ],
    }


def _parameters() -> dict:
    return {
        "conformsTo": "pic-parameters/0.1.0",
        "parameters": [
            {
                "id": "nz-oia/parameter.limit",
                "label": "Limit",
                "unit": "working_days",
                "calendar": {"timezone": "Pacific/Auckland", "convention": "test"},
                "values": [{"from": "2026-01-01", "to": None, "value": 20, "sourceRefs": ["test"]}],
            }
        ],
    }


def _fixtures(pic_id: str = "nz-oia/variable.amount", value: dict | None = None) -> dict:
    return {
        "conformsTo": "pic-fixtures/0.1.0",
        "provenance": {
            "curator": "test",
            "method": "ai-proposed",
            "source": "test",
            "interpreterOfRecord": "test",
            "disclaimer": "Interpretation, not law.",
        },
        "cases": [
            {
                "caseId": "nz-oia/fixture.case",
                "description": "case",
                "period": "2026",
                "entities": {},
                "inputs": {
                    pic_id: value
                    or {"value": "1.00", "valueState": "known", "currency": "NZD"}
                },
                "expected": {},
                "sourceRefs": ["test"],
            }
        ],
    }


def _trace(parameter_id: str = "nz-oia/parameter.limit") -> dict:
    return {
        "conformsTo": "pic-traces/0.1.0",
        "caseId": "nz-oia/fixture.case",
        "packageRef": {"id": "test", "version": "0.1.0"},
        "engine": {"name": "test", "version": "0.1.0"},
        "timestamp": "2026-07-05T00:00:00Z",
        "inputs": {},
        "outputs": {},
        "steps": [
            {
                "stepId": "s1",
                "kind": "decision",
                "refs": {},
                "inputsUsed": [],
                "parameterVersions": [{"id": parameter_id, "effectiveFrom": "2026-01-01"}],
                "result": {"valueState": "unknown"},
                "sourceRefs": ["test"],
            }
        ],
    }


def test_detects_each_contract_type() -> None:
    assert detect_contract({"valueState": "known"}) == "pic-semantics"
    assert detect_contract({"conformsTo": "pic-crosswalk/0.1.0"}) == "pic-crosswalk"
    assert detect_contract({"conformsTo": "pic-parameters/0.1.0"}) == "pic-parameters"
    assert detect_contract({"conformsTo": "pic-fixtures/0.1.0"}) == "pic-fixtures"
    assert detect_contract({"conformsTo": "pic-traces/0.1.0"}) == "pic-traces"


def test_directory_referential_integrity_passes_valid_package(tmp_path: Path) -> None:
    _write(tmp_path / "crosswalk.json", _crosswalk())
    _write(tmp_path / "parameters.json", _parameters())
    _write(tmp_path / "fixtures.json", _fixtures())
    _write(tmp_path / "trace.json", _trace())
    assert validate_path(tmp_path).ok


def test_directory_catches_unknown_fixture_id(tmp_path: Path) -> None:
    _write(tmp_path / "crosswalk.json", _crosswalk())
    _write(tmp_path / "parameters.json", _parameters())
    _write(tmp_path / "fixtures.json", _fixtures("nz-oia/variable.unknown"))
    report = validate_path(tmp_path)
    assert not report.ok
    assert any("unknown crosswalk ID" in issue.message for issue in report.issues)


def test_directory_catches_unknown_trace_parameter(tmp_path: Path) -> None:
    _write(tmp_path / "crosswalk.json", _crosswalk())
    _write(tmp_path / "parameters.json", _parameters())
    _write(tmp_path / "trace.json", _trace("nz-oia/parameter.unknown"))
    report = validate_path(tmp_path)
    assert not report.ok
    assert any("unknown parameter ID" in issue.message for issue in report.issues)


def test_directory_catches_crosswalk_fixture_type_mismatch(tmp_path: Path) -> None:
    _write(tmp_path / "crosswalk.json", _crosswalk("boolean"))
    _write(tmp_path / "parameters.json", _parameters())
    _write(tmp_path / "fixtures.json", _fixtures())
    report = validate_path(tmp_path)
    assert not report.ok
    assert any("type mismatch" in issue.message for issue in report.issues)


def test_cli_returns_nonzero_on_invalid_file(tmp_path: Path) -> None:
    _write(tmp_path / "bad.json", {"conformsTo": "pic-traces/0.1.0"})
    assert main([str(tmp_path / "bad.json"), "--json"]) == 1


def test_nz_oia_clocks_worked_example_validates() -> None:
    path = Path("../../contracts/examples/nz-oia-clocks")
    assert validate_path(path).ok
