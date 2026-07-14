"""Deterministic validation of process-mappings contract consumption."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from pic_contracts.validation import validate_file

_CONTRACT = "pic-process-profile/0.1.0"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class ConsumptionReport:
    """Stable result for a process-mappings consumption check."""

    ok: bool
    errors: tuple[str, ...] = ()
    contract_version: str | None = None
    validated_examples: tuple[str, ...] = ()


def validate_consumption(manifest_path: Path, root: Path) -> ConsumptionReport:
    """Validate a local, pinned contract consumption manifest.

    This deliberately performs no network access. The full upstream commit and
    schema digest make the consumed contract explicit and make local drift fail.
    """

    errors: list[str] = []
    validated_examples: list[str] = []
    try:
        document = _load_object(manifest_path)
    except ValueError as exc:
        return ConsumptionReport(False, (str(exc),))

    contract = document.get("contract")
    if not isinstance(contract, dict):
        errors.append("contract must be an object")
        contract = {}

    if contract.get("conformsTo") != _CONTRACT:
        errors.append(f"contract must consume {_CONTRACT}")
    commit = contract.get("commit")
    if not isinstance(commit, str) or not _COMMIT.fullmatch(commit):
        errors.append("contract commit must be a full 40-character lowercase SHA")
    schema_path = contract.get("schemaPath")
    if not isinstance(schema_path, str):
        errors.append("contract schemaPath must be a relative path")
        schema_path = ""
    schema_sha = contract.get("schemaSha256")
    if not isinstance(schema_sha, str) or not _SHA256.fullmatch(schema_sha):
        errors.append("contract schemaSha256 must be a lowercase SHA-256 digest")

    schema_file = _rooted(root, schema_path, errors, "schema")
    if schema_file is not None and isinstance(schema_sha, str) and _SHA256.fullmatch(schema_sha):
        actual_sha = hashlib.sha256(schema_file.read_bytes()).hexdigest()
        if actual_sha != schema_sha:
            errors.append(f"schema digest mismatch: expected {schema_sha}, got {actual_sha}")

    source_manifest_path = document.get("profileSourceManifest")
    source_manifest_file = _rooted(root, source_manifest_path, errors, "profile source manifest")
    source_manifest = None
    if source_manifest_file is not None:
        try:
            source_manifest = _load_object(source_manifest_file)
        except ValueError as exc:
            errors.append(str(exc))
    if source_manifest is not None:
        source_contract = source_manifest.get("contract")
        if not isinstance(source_contract, dict):
            errors.append("profile source manifest contract must be an object")
        else:
            if source_contract.get("conformsTo") != _CONTRACT:
                errors.append("profile source manifest contract does not match consumption")
            if source_contract.get("commit") != commit:
                errors.append("profile source manifest contract commit does not match consumption")
        if source_manifest.get("promotionBoundary") is None:
            errors.append("profile source manifest must declare a promotion boundary")
        for index, source in enumerate(source_manifest.get("sources", [])):
            if source.get("reviewerState") != "agent-proposed":
                errors.append(f"source assertion {index} is not agent-proposed")

    examples = document.get("examples")
    if not isinstance(examples, list) or not examples:
        errors.append("examples must be a non-empty list")
        examples = []
    for relative in examples:
        if not isinstance(relative, str):
            errors.append("example paths must be strings")
            continue
        example = _rooted(root, relative, errors, "example")
        if example is None:
            continue
        report = validate_file(example)
        if not report.ok:
            errors.extend(f"{relative}: {issue.message}" for issue in report.issues)
        else:
            validated_examples.append(relative)

    evidence_sources = document.get("evidenceSources")
    if not isinstance(evidence_sources, list) or not evidence_sources:
        errors.append("evidenceSources must be a non-empty list")
        evidence_sources = []
    for relative in evidence_sources:
        if isinstance(relative, str):
            _rooted(root, relative, errors, "evidence source")
        else:
            errors.append("evidence source paths must be strings")

    return ConsumptionReport(
        not errors,
        tuple(sorted(set(errors))),
        "0.1.0" if contract.get("conformsTo") == _CONTRACT else None,
        tuple(sorted(validated_examples)),
    )


def _load_object(path: Path) -> dict:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise ValueError(f"manifest must be a JSON object: {path}")
    return document


def _rooted(root: Path, relative: object, errors: list[str], label: str) -> Path | None:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        errors.append(f"{label} path must be relative")
        return None
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label} path escapes repository: {relative}")
        return None
    if not path.exists():
        errors.append(f"{label} not found: {relative}")
        return None
    return path
