from __future__ import annotations

import json
from pathlib import Path

import pytest

from pic_contracts.process_mappings_consumption import _load_object, validate_consumption

ROOT = Path(__file__).parents[3]
MANIFEST = ROOT / "subrepos" / "process-mappings" / "contracts" / "consumption.json"


def test_process_mappings_consumption_manifest_is_current() -> None:
    report = validate_consumption(MANIFEST, ROOT)

    assert report.ok, report.errors
    assert report.contract_version == "0.1.0"


def test_process_mappings_consumption_fails_on_drift(tmp_path: Path) -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    document["contract"]["schemaSha256"] = "0" * 64
    drifted = tmp_path / "consumption.json"
    drifted.write_text(json.dumps(document), encoding="utf-8")

    report = validate_consumption(drifted, ROOT)

    assert not report.ok
    assert any("schema digest" in error for error in report.errors)


@pytest.mark.parametrize(
    "relative",
    [
        "contracts/process-profile/0.1.0/examples/valid/foi-oia.json",
        "contracts/process-profile/0.1.0/examples/valid/human-review.json",
    ],
)
def test_pinned_contract_examples_are_valid(relative: str) -> None:
    report = validate_consumption(MANIFEST, ROOT)

    assert relative in report.validated_examples


def test_portable_evidence_sources_are_immutable() -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert document["portableEvidenceSources"]
    assert all(
        "/447920b9bb72830f2c8490ee40bdcd73c5eedb4a/" in source
        for source in document["portableEvidenceSources"]


def test_load_object_success(tmp_path: Path) -> None:
    manifest_path = tmp_path / "valid.json"
    manifest_path.write_text('{"key": "value"}', encoding="utf-8")
    result = _load_object(manifest_path)
    assert result == {"key": "value"}


def test_load_object_file_not_found(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"
    with pytest.raises(ValueError, match="manifest not found:"):
        _load_object(missing_path)


def test_load_object_invalid_json(tmp_path: Path) -> None:
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text('{invalid_json: true}', encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON in"):
        _load_object(invalid_path)


def test_load_object_not_a_dict(tmp_path: Path) -> None:
    array_path = tmp_path / "array.json"
    array_path.write_text('["not", "a", "dict"]', encoding="utf-8")
    with pytest.raises(ValueError, match="manifest must be a JSON object:"):
        _load_object(array_path)
