from __future__ import annotations

import json
from pathlib import Path
import pytest

from pic_contracts.process_mappings_consumption import validate_consumption

ROOT = Path(__file__).parents[3]
MANIFEST = ROOT / "subrepos" / "process-mappings" / "contracts" / "consumption.json"

@pytest.fixture
def base_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def test_missing_manifest(tmp_path: Path) -> None:
    report = validate_consumption(tmp_path / "missing.json", ROOT)
    assert not report.ok
    assert any("manifest not found" in err for err in report.errors)

def test_invalid_json_manifest(tmp_path: Path) -> None:
    manifest_path = tmp_path / "invalid.json"
    manifest_path.write_text("{invalid json", encoding="utf-8")
    report = validate_consumption(manifest_path, ROOT)
    assert not report.ok
    assert any("invalid JSON" in err for err in report.errors)

def test_manifest_not_object(tmp_path: Path) -> None:
    manifest_path = tmp_path / "not_object.json"
    manifest_path.write_text("[]", encoding="utf-8")
    report = validate_consumption(manifest_path, ROOT)
    assert not report.ok
    assert any("manifest must be a JSON object" in err for err in report.errors)

def _write_and_test(tmp_path, manifest, root=ROOT) -> tuple[bool, tuple[str, ...]]:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    report = validate_consumption(manifest_path, root)
    return report.ok, report.errors

def test_contract_must_be_object(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"] = "not an object"
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "contract must be an object" in errors

def test_contract_conforms_to(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"]["conformsTo"] = "invalid"
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "contract must consume pic-process-profile/0.1.0" in errors

def test_contract_commit_invalid(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"]["commit"] = "short"
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "contract commit must be a full 40-character lowercase SHA" in errors

    base_manifest["contract"]["commit"] = 123
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "contract commit must be a full 40-character lowercase SHA" in errors

def test_schema_path_invalid(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"]["schemaPath"] = 123
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "contract schemaPath must be a relative path" in errors

def test_schema_sha_invalid(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"]["schemaSha256"] = "invalid"
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "contract schemaSha256 must be a lowercase SHA-256 digest" in errors

    base_manifest["contract"]["schemaSha256"] = 123
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "contract schemaSha256 must be a lowercase SHA-256 digest" in errors

def test_schema_path_absolute(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"]["schemaPath"] = "/absolute/path.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert "schema path must be relative" in errors

def test_schema_path_escapes(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"]["schemaPath"] = "../outside.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert any("schema path escapes repository" in err for err in errors)

def test_schema_path_not_found(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["contract"]["schemaPath"] = "nonexistent.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert any("schema not found: nonexistent.json" in err for err in errors)


def test_source_manifest_not_object(tmp_path: Path, base_manifest: dict) -> None:
    source_manifest_path = tmp_path / "source_manifest.json"
    source_manifest_path.write_text("[]", encoding="utf-8")
    base_manifest["profileSourceManifest"] = "source_manifest.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert any("manifest must be a JSON object" in err for err in errors)

def test_source_manifest_contract_not_object(tmp_path: Path, base_manifest: dict) -> None:
    source_manifest = {"contract": "not an object", "promotionBoundary": "boundary", "sources": []}
    source_manifest_path = tmp_path / "source_manifest.json"
    source_manifest_path.write_text(json.dumps(source_manifest), encoding="utf-8")
    base_manifest["profileSourceManifest"] = "source_manifest.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert "profile source manifest contract must be an object" in errors

def test_source_manifest_contract_mismatch(tmp_path: Path, base_manifest: dict) -> None:
    source_manifest = {"contract": {"conformsTo": "invalid", "commit": "invalid"}, "promotionBoundary": "boundary", "sources": []}
    source_manifest_path = tmp_path / "source_manifest.json"
    source_manifest_path.write_text(json.dumps(source_manifest), encoding="utf-8")
    base_manifest["profileSourceManifest"] = "source_manifest.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert "profile source manifest contract does not match consumption" in errors
    assert "profile source manifest contract commit does not match consumption" in errors

def test_source_manifest_no_promotion_boundary(tmp_path: Path, base_manifest: dict) -> None:
    source_manifest = {"contract": base_manifest["contract"].copy(), "sources": []}
    source_manifest_path = tmp_path / "source_manifest.json"
    source_manifest_path.write_text(json.dumps(source_manifest), encoding="utf-8")
    base_manifest["profileSourceManifest"] = "source_manifest.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert "profile source manifest must declare a promotion boundary" in errors

def test_source_manifest_source_not_agent_proposed(tmp_path: Path, base_manifest: dict) -> None:
    source_manifest = {"contract": base_manifest["contract"].copy(), "promotionBoundary": "boundary", "sources": [{"reviewerState": "invalid"}]}
    source_manifest_path = tmp_path / "source_manifest.json"
    source_manifest_path.write_text(json.dumps(source_manifest), encoding="utf-8")
    base_manifest["profileSourceManifest"] = "source_manifest.json"
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert "source assertion 0 is not agent-proposed" in errors

def test_examples_not_list(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["examples"] = "not a list"
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "examples must be a non-empty list" in errors

def test_examples_empty_list(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["examples"] = []
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "examples must be a non-empty list" in errors

def test_examples_not_strings(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["examples"] = [123]
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "example paths must be strings" in errors

def test_example_validation_fails(tmp_path: Path, base_manifest: dict) -> None:
    example_path = tmp_path / "example.json"
    example_path.write_text("{invalid json", encoding="utf-8")
    base_manifest["examples"] = ["example.json"]
    ok, errors = _write_and_test(tmp_path, base_manifest, root=tmp_path)
    assert not ok
    assert any("example.json" in err and "JSON" in err for err in errors)

def test_evidence_sources_not_list(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["evidenceSources"] = "not a list"
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "evidenceSources must be a non-empty list" in errors

def test_evidence_sources_empty_list(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["evidenceSources"] = []
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "evidenceSources must be a non-empty list" in errors

def test_evidence_sources_not_strings(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["evidenceSources"] = [123]
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "evidence source paths must be strings" in errors

def test_portable_evidence_sources_not_list(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["portableEvidenceSources"] = "not a list"
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "portableEvidenceSources must be a non-empty list" in errors

def test_portable_evidence_sources_empty_list(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["portableEvidenceSources"] = []
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "portableEvidenceSources must be a non-empty list" in errors

def test_portable_evidence_sources_invalid_url(tmp_path: Path, base_manifest: dict) -> None:
    base_manifest["portableEvidenceSources"] = ["https://github.com/edithatogo/foi-o/tree/invalid/file.json"]
    ok, errors = _write_and_test(tmp_path, base_manifest)
    assert not ok
    assert "portable evidence sources must be pinned FOI-O blob/tree URLs" in errors
