"""Validate the incubator's released-contract and source provenance manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parents[1] / "contracts/tools/src"))

from pic_contracts.validation import validate_file


SHA256 = re.compile(r"^[0-9a-f]{64}$")
IMMUTABLE = re.compile(r"^(?:v[0-9]+\.[0-9]+\.[0-9]+|[0-9a-f]{40})$")


def _pinned_digest(repository_root: Path, revision: str, path: str) -> str | None:
    """Hash a file from the recorded Git revision, never from a newer checkout."""
    try:
        content = subprocess.check_output(
            ["git", "-C", str(repository_root), "show", f"{revision}:{path}"],
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return hashlib.sha256(content).hexdigest()


def _immutable(value: Any) -> bool:
    return isinstance(value, str) and bool(IMMUTABLE.fullmatch(value))


def validate_manifest(manifest_path: Path, repository_root: Path) -> list[str]:
    """Return deterministic diagnostics for a contract-consumption manifest."""
    try:
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"manifest cannot be read: {exc}"]

    errors: list[str] = []
    if document.get("schemaVersion") != "process-mappings-contract-consumption.v0.1.0":
        errors.append("manifest schemaVersion is unsupported")

    repository = document.get("repository")
    if not isinstance(repository, dict) or repository.get("name") != "edithatogo/rac-conformance":
        errors.append("repository must identify edithatogo/rac-conformance")
    elif not _immutable(repository.get("revision")):
        errors.append("repository revision must be immutable")

    contracts = document.get("normativeContracts")
    if not isinstance(contracts, list) or not contracts:
        errors.append("normativeContracts must be a non-empty list")
        contracts = []
    seen: set[str] = set()
    for index, contract in enumerate(contracts):
        location = f"normativeContracts[{index}]"
        if not isinstance(contract, dict):
            errors.append(f"{location} must be an object")
            continue
        identifier = contract.get("id")
        path_value = contract.get("path")
        digest = contract.get("sha256")
        if not isinstance(identifier, str) or identifier in seen:
            errors.append(f"{location} has a missing or duplicate id")
        else:
            seen.add(identifier)
        if not isinstance(path_value, str) or not path_value.startswith("contracts/"):
            errors.append(f"{location} must reference a parent contracts path")
            continue
        if not isinstance(identifier, str) or path_value != f"contracts/{identifier}/schema.json":
            errors.append(f"{location} path must match its contract id")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            errors.append(f"{location} has an invalid sha256")
            continue
        revision = repository.get("revision") if isinstance(repository, dict) else None
        actual_digest = (
            _pinned_digest(repository_root, revision, path_value)
            if isinstance(revision, str)
            else None
        )
        if actual_digest is None:
            errors.append(f"{location} schema is missing: {path_value}")
        elif actual_digest != digest:
            errors.append(f"{location} schema digest mismatch")

    inputs = document.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        errors.append("inputs must be a non-empty list")
        inputs = []
    input_ids: set[str] = set()
    for index, source in enumerate(inputs):
        location = f"inputs[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{location} must be an object")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or source_id in input_ids:
            errors.append(f"{location} has a missing or duplicate id")
        elif source_id:
            input_ids.add(source_id)
        if source.get("repository") not in {"edithatogo/foi-o", "edithatogo/foi-process"}:
            errors.append(f"{location} repository is outside the declared integration boundary")
        if not _immutable(source.get("revision")):
            errors.append(f"{location} input revision must be immutable")
        if not isinstance(source.get("path"), str) or not source["path"]:
            errors.append(f"{location} must record a source path")
        digest = source.get("sha256")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            errors.append(f"{location} has an invalid sha256")
        if source.get("status") != "observed" or source.get("method") != "official-schema":
            errors.append(f"{location} must remain an observed official-schema assertion")

    matrix = document.get("compatibilityMatrix")
    if not isinstance(matrix, list) or {row.get("consumer") for row in matrix if isinstance(row, dict)} != {"foi-o", "foi-process"}:
        errors.append("compatibilityMatrix must cover both foi-o and foi-process")
    for index, row in enumerate(matrix or []):
        if not isinstance(row, dict) or not row.get("contractIds") or not row.get("inputIds"):
            errors.append(f"compatibilityMatrix[{index}] must link contracts and inputs")
        elif not set(row["inputIds"]).issubset(input_ids):
            errors.append(f"compatibilityMatrix[{index}] references an unknown input")

    return errors


def validate_candidate_profiles(repository_root: Path) -> list[str]:
    """Validate incubator profile candidates against the parent process contract."""
    errors: list[str] = []
    candidate_root = repository_root / "subrepos/process-mappings/profiles"
    for path in sorted(candidate_root.glob("**/candidates/*.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: cannot read candidate: {exc}")
            continue
        # Mapping ledgers and source assertion ledgers are inputs to profiles,
        # not PIC process-profile documents themselves.
        if not isinstance(document, dict) or not isinstance(document.get("conformsTo"), str):
            continue
        report = validate_file(path)
        errors.extend(
            f"{path}: {issue.code}: {issue.message}" for issue in report.issues
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", default="subrepos/process-mappings/schemas/contract-consumption.json")
    parser.add_argument("--repository-root", default=".")
    args = parser.parse_args(argv)
    errors = validate_manifest(Path(args.manifest), Path(args.repository_root))
    errors.extend(validate_candidate_profiles(Path(args.repository_root)))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
