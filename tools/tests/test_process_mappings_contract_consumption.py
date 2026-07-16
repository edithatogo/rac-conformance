"""Tests for the process-mappings contract consumption manifest."""

from __future__ import annotations

import json
from pathlib import Path

from tools.validate_process_mappings_contracts import validate_candidate_profiles, validate_manifest


ROOT = Path(__file__).parents[2]
MANIFEST = ROOT / "subrepos/process-mappings/schemas/contract-consumption.json"


def test_checked_in_manifest_validates_against_local_contracts() -> None:
    errors = validate_manifest(MANIFEST, ROOT)
    assert errors == []


def test_manifest_rejects_mutable_contract_revision(tmp_path: Path) -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    document["repository"]["revision"] = "main"
    candidate = tmp_path / "manifest.json"
    candidate.write_text(json.dumps(document), encoding="utf-8")

    errors = validate_manifest(candidate, ROOT)

    assert any("immutable" in error for error in errors)


def test_manifest_rejects_schema_digest_drift(tmp_path: Path) -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    document["normativeContracts"][0]["sha256"] = "0" * 64
    candidate = tmp_path / "manifest.json"
    candidate.write_text(json.dumps(document), encoding="utf-8")

    errors = validate_manifest(candidate, ROOT)

    assert any("digest mismatch" in error for error in errors)


def test_manifest_requires_immutable_external_input_provenance(tmp_path: Path) -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    document["inputs"][0]["revision"] = "latest"
    candidate = tmp_path / "manifest.json"
    candidate.write_text(json.dumps(document), encoding="utf-8")

    errors = validate_manifest(candidate, ROOT)

    assert any("input revision" in error for error in errors)


def test_candidate_profiles_validate_against_parent_contract() -> None:
    assert validate_candidate_profiles(ROOT) == []
