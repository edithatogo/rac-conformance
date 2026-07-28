from __future__ import annotations

import json
from pathlib import Path

import pytest

from pic_contracts.process_mappings_consumption import _rooted, validate_consumption

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
    )


def test_rooted_happy_path(tmp_path: Path) -> None:
    test_file = tmp_path / "test.txt"
    test_file.touch()
    errors = []
    result = _rooted(tmp_path, "test.txt", errors, "test_label")
    assert result == test_file.resolve()
    assert not errors

def test_rooted_not_a_string(tmp_path: Path) -> None:
    errors = []
    result = _rooted(tmp_path, None, errors, "test_label")
    assert result is None
    assert errors == ["test_label path must be relative"]

def test_rooted_empty_string(tmp_path: Path) -> None:
    errors = []
    result = _rooted(tmp_path, "", errors, "test_label")
    assert result is None
    assert errors == ["test_label path must be relative"]

def test_rooted_absolute_path(tmp_path: Path) -> None:
    errors = []
    result = _rooted(tmp_path, "/absolute/path", errors, "test_label")
    assert result is None
    assert errors == ["test_label path must be relative"]

def test_rooted_escapes_repository(tmp_path: Path) -> None:
    errors = []
    result = _rooted(tmp_path, "../outside.txt", errors, "test_label")
    assert result is None
    assert errors == ["test_label path escapes repository: ../outside.txt"]

def test_rooted_file_not_found(tmp_path: Path) -> None:
    errors = []
    result = _rooted(tmp_path, "does_not_exist.txt", errors, "test_label")
    assert result is None
    assert errors == ["test_label not found: does_not_exist.txt"]
