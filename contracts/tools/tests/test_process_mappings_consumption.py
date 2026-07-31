from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from pic_contracts.process_mappings_consumption import validate_consumption

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


# --- New Tests for Full Coverage ---


def _modify_and_validate(
    tmp_path: Path, modifier: Callable[[dict[str, Any]], None]
) -> tuple[bool, tuple[str, ...]]:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    modifier(document)
    drifted = tmp_path / "consumption.json"
    drifted.write_text(json.dumps(document), encoding="utf-8")
    report = validate_consumption(drifted, ROOT)
    return report.ok, report.errors


def test_load_object_failures(tmp_path: Path) -> None:
    # File not found
    report = validate_consumption(tmp_path / "non_existent.json", ROOT)
    assert not report.ok
    assert any("manifest not found" in e for e in report.errors)

    # Invalid JSON
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{", encoding="utf-8")
    report = validate_consumption(invalid, ROOT)
    assert not report.ok
    assert any("invalid JSON" in e for e in report.errors)

    # Not a dict
    not_dict = tmp_path / "not_dict.json"
    not_dict.write_text("[]", encoding="utf-8")
    report = validate_consumption(not_dict, ROOT)
    assert not report.ok
    assert any("manifest must be a JSON object" in e for e in report.errors)


def test_invalid_contract(tmp_path: Path) -> None:
    def drop_contract(d: dict[str, Any]) -> None:
        d["contract"] = "not a dict"

    ok, errors = _modify_and_validate(tmp_path, drop_contract)
    assert not ok
    assert "contract must be an object" in errors

    def invalid_conformsTo(d: dict[str, Any]) -> None:
        d["contract"]["conformsTo"] = "wrong"

    ok, errors = _modify_and_validate(tmp_path, invalid_conformsTo)
    assert not ok
    assert "contract must consume pic-process-profile/0.1.0" in errors

    def invalid_commit(d: dict[str, Any]) -> None:
        d["contract"]["commit"] = "short"

    ok, errors = _modify_and_validate(tmp_path, invalid_commit)
    assert not ok
    assert "contract commit must be a full 40-character lowercase SHA" in errors

    def invalid_schema_path(d: dict[str, Any]) -> None:
        d["contract"]["schemaPath"] = 123

    ok, errors = _modify_and_validate(tmp_path, invalid_schema_path)
    assert not ok
    assert "contract schemaPath must be a relative path" in errors

    def invalid_schema_sha(d: dict[str, Any]) -> None:
        d["contract"]["schemaSha256"] = "short"

    ok, errors = _modify_and_validate(tmp_path, invalid_schema_sha)
    assert not ok
    assert "contract schemaSha256 must be a lowercase SHA-256 digest" in errors


def test_source_manifest_validation(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()

    # We will build a complete mock directory structure to test everything

    # Setup schema
    schema_path = "schema.json"
    schema_file = root / schema_path
    schema_file.write_text("{}", encoding="utf-8")
    import hashlib

    schema_sha = hashlib.sha256(schema_file.read_bytes()).hexdigest()

    commit = "1234567890abcdef1234567890abcdef12345678"

    # Base valid document
    def get_valid_doc():
        return {
            "contract": {
                "conformsTo": "pic-process-profile/0.1.0",
                "commit": commit,
                "schemaPath": schema_path,
                "schemaSha256": schema_sha,
            },
            "profileSourceManifest": "source_manifest.json",
            "examples": ["example1.json"],
            "evidenceSources": ["evidence1.json"],
            "portableEvidenceSources": [
                "https://github.com/edithatogo/foi-o/tree/1234567890abcdef1234567890abcdef12345678/path"
            ],
        }

    # Setup example
    example_path = root / "example1.json"
    # validate_file will likely fail, but that's ok we test the error
    example_path.write_text('{"foo": "bar"}', encoding="utf-8")

    # Setup evidence
    evidence_path = root / "evidence1.json"
    evidence_path.write_text("test", encoding="utf-8")

    # Helper to test permutations
    def check(doc, source_manifest_content, expected_error_substrings):
        manifest_path = root / "consumption.json"
        manifest_path.write_text(json.dumps(doc), encoding="utf-8")

        if source_manifest_content is not None:
            if isinstance(source_manifest_content, str):
                (root / "source_manifest.json").write_text(
                    source_manifest_content, encoding="utf-8"
                )
            else:
                (root / "source_manifest.json").write_text(
                    json.dumps(source_manifest_content), encoding="utf-8"
                )
        else:
            if (root / "source_manifest.json").exists():
                (root / "source_manifest.json").unlink()

        report = validate_consumption(manifest_path, root)

        for substring in expected_error_substrings:
            assert any(substring in e for e in report.errors), (
                f"Expected '{substring}' in {report.errors}"
            )

    # 1. source manifest not found (caught by _rooted,
    # but validate_consumption just adds error and continues)
    doc = get_valid_doc()
    check(doc, None, ["profile source manifest not found"])

    # 2. source manifest invalid JSON
    check(doc, "{", ["invalid JSON"])

    # 3. source manifest not a dict
    check(doc, "[]", ["manifest must be a JSON object"])

    # 4. source contract missing/not dict
    check(doc, {"contract": "not a dict"}, ["profile source manifest contract must be an object"])

    # 5. source contract conformsTo mismatch
    check(
        doc,
        {"contract": {"conformsTo": "wrong", "commit": commit}},
        ["profile source manifest contract does not match consumption"],
    )

    # 6. source contract commit mismatch
    check(
        doc,
        {"contract": {"conformsTo": "pic-process-profile/0.1.0", "commit": "wrong"}},
        ["profile source manifest contract commit does not match consumption"],
    )

    # 7. missing promotion boundary
    check(
        doc,
        {"contract": {"conformsTo": "pic-process-profile/0.1.0", "commit": commit}},
        ["profile source manifest must declare a promotion boundary"],
    )

    # 8. invalid reviewer state
    check(
        doc,
        {
            "contract": {"conformsTo": "pic-process-profile/0.1.0", "commit": commit},
            "promotionBoundary": "boundary",
            "sources": [{"reviewerState": "wrong"}],
        },
        ["source assertion 0 is not agent-proposed"],
    )

    # Examples testing
    # 9. examples not list
    doc = get_valid_doc()
    doc["examples"] = "not a list"
    check(doc, "{}", ["examples must be a non-empty list"])

    # 10. examples not string
    doc = get_valid_doc()
    doc["examples"] = [123]
    check(doc, "{}", ["example paths must be strings"])

    # 11. examples invalid validation
    # (this uses validate_file which requires JSON schema validation usually)
    doc = get_valid_doc()
    doc["examples"] = ["example1.json"]
    # validate_file will fail because it's not a valid contract example,
    # we'll see if it adds to errors
    # Wait, the error might be specific to validate_file output.
    # We can just check that report.ok is false.
    manifest_path = root / "consumption.json"
    manifest_path.write_text(json.dumps(doc), encoding="utf-8")
    (root / "source_manifest.json").write_text("{}", encoding="utf-8")
    report = validate_consumption(manifest_path, root)
    assert not report.ok

    # Evidence sources testing
    # 12. evidenceSources not list
    doc = get_valid_doc()
    doc["evidenceSources"] = "not a list"
    check(doc, "{}", ["evidenceSources must be a non-empty list"])

    # 13. evidenceSources not string
    doc = get_valid_doc()
    doc["evidenceSources"] = [123]
    check(doc, "{}", ["evidence source paths must be strings"])

    # Portable evidence sources testing
    # 14. portableEvidenceSources not list
    doc = get_valid_doc()
    doc["portableEvidenceSources"] = "not a list"
    check(doc, "{}", ["portableEvidenceSources must be a non-empty list"])

    # 15. portableEvidenceSources invalid format
    doc = get_valid_doc()
    doc["portableEvidenceSources"] = ["invalid-url"]
    check(doc, "{}", ["portable evidence sources must be pinned FOI-O blob/tree URLs"])


def test_rooted_edge_cases(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()

    commit = "1234567890abcdef1234567890abcdef12345678"
    schema_sha = "0" * 64

    doc = {
        "contract": {
            "conformsTo": "pic-process-profile/0.1.0",
            "commit": commit,
            "schemaPath": "/absolute/path",
            "schemaSha256": schema_sha,
        },
        "profileSourceManifest": "../escaped_path",
        "examples": ["example1.json"],
        "evidenceSources": ["evidence1.json"],
        "portableEvidenceSources": [
            "https://github.com/edithatogo/foi-o/tree/1234567890abcdef1234567890abcdef12345678/path"
        ],
    }

    manifest_path = root / "consumption.json"
    manifest_path.write_text(json.dumps(doc), encoding="utf-8")

    report = validate_consumption(manifest_path, root)
    assert not report.ok
    assert any("schema path must be relative" in e for e in report.errors)
    assert any("profile source manifest path escapes repository" in e for e in report.errors)
