#!/usr/bin/env python3
"""Verify artifact-backed independent-validation evidence fail closed."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor/tracks/v1_independent_validation_20260714"
SCHEMA = TRACK / "SUBMISSION_SCHEMA.json"
CRITERIA = TRACK / "INDEPENDENCE_CRITERIA.json"
KIT = ROOT / "independent/kit"
TRUSTED_ATTESTATIONS = ROOT / "independent/TRUSTED_ATTESTATIONS.json"
NONQUALIFYING_OUTCOMES = {"partial", "conflicting", "withdrawn", "declined", "unresponsive"}


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    document = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"duplicate JSON key: {key}")
        document[key] = value
    return document


def _load_json(path: Path) -> object:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
    )


def _kit_digest(manifest: dict) -> str:
    digest = hashlib.sha256()
    for artifact in manifest["artifacts"]:
        digest.update(artifact["path"].encode())
        digest.update(b"\0")
        digest.update(artifact["sha256"].encode())
        digest.update(b"\n")
    return digest.hexdigest()


def _verify_kit_artifacts(manifest: dict) -> list[str]:
    diagnostics = []
    for artifact in manifest["artifacts"]:
        path = (KIT / artifact["path"]).resolve()
        if KIT.resolve() not in path.parents or not path.is_file():
            diagnostics.append(f"kit artifact is missing or unsafe: {artifact['path']}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != artifact["sha256"]:
            diagnostics.append(f"kit artifact digest mismatch: {artifact['path']}")
    return diagnostics


def _verify_artifact(name: str, artifact: dict, evidence_root: Path) -> str | None:
    root = evidence_root.resolve()
    path = (root / artifact["path"]).resolve()
    if path == root or root not in path.parents:
        return f"{name} artifact path escapes evidence root"
    if not path.is_file():
        return f"{name} artifact is missing"
    content = path.read_bytes()
    if not content:
        return f"{name} artifact is empty"
    actual = "sha256:" + hashlib.sha256(content).hexdigest()
    if actual != artifact["sha256"]:
        return f"{name} artifact digest mismatch"
    return None


def classify(
    packet: dict,
    *,
    evidence_root: Path | None = None,
    today: dt.date | None = None,
    trusted_attestations: set[str] | None = None,
) -> dict:
    """Return structural, evidence, and release-qualification status."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(packet),
        key=lambda error: list(error.path),
    )
    schema_diagnostics = [
        "schema: " + "/".join(map(str, error.path)) + ": " + error.message
        for error in errors
    ]
    if schema_diagnostics:
        return {
            "schemaValid": False,
            "evidenceVerified": False,
            "status": "rejected",
            "exceptions": schema_diagnostics,
            "qualifiesForV1": False,
            "expiresAt": None,
        }

    today = today or dt.date.today()
    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    manifest = json.loads((KIT / "manifest.json").read_text(encoding="utf-8"))
    if trusted_attestations is None:
        trust = json.loads(TRUSTED_ATTESTATIONS.read_text(encoding="utf-8"))
        trusted_attestations = set(trust["approvedSha256"])
    verification_exceptions: list[str] = []
    qualification_exceptions: list[str] = []

    expected_kit_digest = _kit_digest(manifest)
    verification_exceptions.extend(_verify_kit_artifacts(manifest))
    if packet["kitDigestSha256"] != expected_kit_digest:
        verification_exceptions.append("kit digest mismatch")
    if packet["contractVersions"] != [manifest["contract"]]:
        verification_exceptions.append("contract versions do not match the canonical kit")

    result_artifact_verified = False
    if evidence_root is None:
        verification_exceptions.append("evidence root is required")
    else:
        artifact_paths = [artifact["path"] for artifact in packet["artifacts"].values()]
        if len(artifact_paths) != len(set(artifact_paths)):
            verification_exceptions.append("artifact roles do not reference distinct paths")
        for name, artifact in packet["artifacts"].items():
            diagnostic = _verify_artifact(name, artifact, evidence_root)
            if diagnostic:
                verification_exceptions.append(diagnostic)
            elif name == "result":
                result_artifact_verified = True

    expected_cases = {
        artifact["path"]
        for artifact in manifest["artifacts"]
        if artifact["role"] in {"valid", "invalid"}
    }
    case_ids = [result["caseId"] for result in packet["tests"]]
    if len(case_ids) != len(set(case_ids)):
        verification_exceptions.append("test case identifiers are duplicated")
    missing = sorted(expected_cases - set(case_ids))
    unexpected = sorted(set(case_ids) - expected_cases)
    if missing:
        verification_exceptions.append("test cases are missing: " + ", ".join(missing))
    if unexpected:
        verification_exceptions.append("test cases are unexpected: " + ", ".join(unexpected))
    if any(result["status"] != "pass" for result in packet["tests"]):
        verification_exceptions.append("one or more test cases did not pass")
    if evidence_root is not None and result_artifact_verified:
        result_path = (evidence_root.resolve() / packet["artifacts"]["result"]["path"]).resolve()
        if result_path.is_file():
            try:
                result_document = _load_json(result_path)
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
                verification_exceptions.append("result artifact is not valid JSON")
            else:
                expected_result = {
                    "schemaVersion": "rac-independent-execution-result.v1",
                    "implementationId": packet["implementationId"],
                    "sourceRevision": packet["sourceRevision"],
                    "kitDigestSha256": packet["kitDigestSha256"],
                    "status": "pass",
                    "tests": packet["tests"],
                }
                if not isinstance(result_document, dict):
                    verification_exceptions.append("result artifact root is not an object")
                elif result_document != expected_result:
                    verification_exceptions.append("result artifact does not match the submitted execution result")

    if evidence_root is not None:
        result_digest = packet["artifacts"]["result"]["sha256"]
        bindings = {
            "acknowledgement": {
                "schemaVersion": "rac-independent-acknowledgement.v1",
                "implementationId": packet["implementationId"],
                "sourceRevision": packet["sourceRevision"],
                "resultSha256": result_digest,
                "status": "confirmed",
            },
            "attestation": {
                "schemaVersion": "rac-independent-attestation.v1",
                "implementationId": packet["implementationId"],
                "sourceRevision": packet["sourceRevision"],
                "resultSha256": result_digest,
                "issuerControl": "external",
            },
        }
        for role, expected in bindings.items():
            path = (evidence_root.resolve() / packet["artifacts"][role]["path"]).resolve()
            if path.is_file():
                try:
                    document = _load_json(path)
                except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
                    verification_exceptions.append(f"{role} artifact is not valid JSON")
                    continue
                if not isinstance(document, dict) or any(
                    document.get(key) != value for key, value in expected.items()
                ):
                    verification_exceptions.append(f"{role} artifact is not bound to the submission")
        if packet["artifacts"]["attestation"]["sha256"] not in trusted_attestations:
            qualification_exceptions.append("attestation is not analyst-trusted")

    if packet["organisation"]["controlRelationship"] != "external":
        qualification_exceptions.append("organisation is not independently controlled")
    if packet["repository"]["accessControl"] != "external":
        qualification_exceptions.append("repository is not independently controlled")
    for dimension, control in packet["independence"].items():
        if control != "external":
            qualification_exceptions.append(f"{dimension} is not independently controlled")
    if packet["execution"]["cleanCheckout"] is not True:
        qualification_exceptions.append("execution was not from a clean checkout")
    if packet["unresolvedMismatches"]:
        qualification_exceptions.append("qualifying result has unresolved mismatches")

    freshness_date = dt.date.fromisoformat(packet["maintenance"]["freshnessDate"])
    freshness_days = criteria["freshness"]["releaseCandidateDays"]
    age = (today - freshness_date).days
    if age < 0 or age > freshness_days:
        qualification_exceptions.append("maintenance evidence is stale or future-dated")
    executed_at = dt.date.fromisoformat(packet["execution"]["executedAt"])
    if executed_at > today:
        qualification_exceptions.append("execution is future-dated")
    if executed_at > freshness_date:
        qualification_exceptions.append("maintenance evidence predates execution")
    expires_at = freshness_date + dt.timedelta(days=freshness_days)

    declared = packet["outcome"]
    if verification_exceptions:
        status = "rejected"
    elif declared in NONQUALIFYING_OUTCOMES:
        status = declared
    elif qualification_exceptions:
        status = "partial"
    else:
        status = "qualifying"
    exceptions = sorted(set(verification_exceptions + qualification_exceptions))
    return {
        "schemaValid": True,
        "evidenceVerified": not verification_exceptions,
        "status": status,
        "exceptions": exceptions,
        "qualifiesForV1": status == "qualifying",
        "expiresAt": expires_at.isoformat(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument(
        "--evidence-root",
        type=Path,
        help="Root for packet-relative evidence artifacts (defaults to packet directory)",
    )
    args = parser.parse_args(argv)
    try:
        packet = _load_json(args.packet)
        result = classify(
            packet,
            evidence_root=args.evidence_root or args.packet.parent,
        )
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        result = {
            "schemaValid": False,
            "evidenceVerified": False,
            "status": "rejected",
            "exceptions": [f"input: {exc}"],
            "qualifiesForV1": False,
            "expiresAt": None,
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["qualifiesForV1"] else 1


if __name__ == "__main__":
    sys.exit(main())
