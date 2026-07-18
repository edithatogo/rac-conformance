import copy
import datetime as dt
import hashlib
import json
from pathlib import Path

from tools.independent_evidence import classify


ROOT = Path(__file__).parents[2]
KIT = ROOT / "independent/kit"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def kit_digest() -> str:
    manifest = json.loads((KIT / "manifest.json").read_text())
    digest = hashlib.sha256()
    for artifact in manifest["artifacts"]:
        digest.update(artifact["path"].encode())
        digest.update(b"\0")
        digest.update(artifact["sha256"].encode())
        digest.update(b"\n")
    return digest.hexdigest()


def packet(tmp_path: Path) -> dict:
    evidence = tmp_path / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((KIT / "manifest.json").read_text())
    cases = [item["path"] for item in manifest["artifacts"] if item["role"] in {"valid", "invalid"}]
    tests = [{"caseId": case, "status": "pass"} for case in cases]
    implementation_id = "external-example"
    source_revision = "a" * 40
    digest = kit_digest()
    (evidence / "source.tar").write_bytes(b"independent source")
    (evidence / "input.json").write_bytes(b"{}\n")
    (evidence / "result.json").write_text(
        json.dumps(
            {
                "schemaVersion": "rac-independent-execution-result.v1",
                "implementationId": implementation_id,
                "sourceRevision": source_revision,
                "kitDigestSha256": digest,
                "status": "pass",
                "tests": tests,
            },
            sort_keys=True,
        )
    )
    result_digest = sha256(evidence / "result.json")
    (evidence / "acknowledgement.json").write_text(
        json.dumps(
            {
                "schemaVersion": "rac-independent-acknowledgement.v1",
                "implementationId": implementation_id,
                "sourceRevision": source_revision,
                "resultSha256": result_digest,
                "status": "confirmed",
                "acknowledgedBy": "Example Org",
                "acknowledgedAt": "2026-07-01",
            },
            sort_keys=True,
        )
    )
    (evidence / "attestation.json").write_text(
        json.dumps(
            {
                "schemaVersion": "rac-independent-attestation.v1",
                "implementationId": implementation_id,
                "sourceRevision": source_revision,
                "resultSha256": result_digest,
                "issuer": "Example Org",
                "issuerControl": "external",
                "attestedAt": "2026-07-01",
            },
            sort_keys=True,
        )
    )
    return {
        "schemaVersion": "rac-independent-submission.v2",
        "implementationId": implementation_id,
        "organisation": {"name": "Example Org", "controlRelationship": "external"},
        "repository": {"url": "https://example.org/repo", "accessControl": "external"},
        "sourceRevision": source_revision,
        "contractVersions": ["pic-semantics/0.1.0"],
        "kitDigestSha256": digest,
        "independence": {
            "codebase": "external",
            "oracle": "external",
            "fixtureCuration": "external",
        },
        "execution": {
            "runtime": "Python 3.14",
            "platform": "test",
            "cleanCheckout": True,
            "executedAt": "2026-07-01",
            "command": ["python", "evaluate.py"],
        },
        "artifacts": {
            name: {"path": f"evidence/{filename}", "sha256": sha256(evidence / filename)}
            for name, filename in {
                "source": "source.tar",
                "input": "input.json",
                "result": "result.json",
                "acknowledgement": "acknowledgement.json",
                "attestation": "attestation.json",
            }.items()
        },
        "tests": tests,
        "outcome": "qualifying",
        "maintenance": {"owner": "Example Org", "freshnessDate": "2026-07-01"},
        "limitations": ["Structural conformance only"],
        "unresolvedMismatches": [],
    }


def classify_packet(candidate: dict, *, evidence_root: Path, today: dt.date) -> dict:
    return classify(
        candidate,
        evidence_root=evidence_root,
        today=today,
        trusted_attestations={candidate["artifacts"]["attestation"]["sha256"]},
    )


def test_artifact_backed_packet_qualifies(tmp_path: Path) -> None:
    result = classify_packet(packet(tmp_path), evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["schemaValid"] is True
    assert result["evidenceVerified"] is True
    assert result["status"] == "qualifying"
    assert result["qualifiesForV1"] is True
    assert result["expiresAt"] == "2026-09-29"


def test_tampered_or_missing_artifact_fails_closed(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    (tmp_path / candidate["artifacts"]["result"]["path"]).write_text("tampered")
    result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "rejected"
    assert result["evidenceVerified"] is False
    assert any("result artifact digest mismatch" in item for item in result["exceptions"])


def test_artifact_roles_must_be_distinct_and_nonempty(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["artifacts"]["input"] = copy.deepcopy(candidate["artifacts"]["source"])
    aliased = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert aliased["status"] == "rejected"
    assert "artifact roles do not reference distinct paths" in aliased["exceptions"]

    candidate = packet(tmp_path)
    attestation = tmp_path / candidate["artifacts"]["attestation"]["path"]
    attestation.write_bytes(b"")
    candidate["artifacts"]["attestation"]["sha256"] = sha256(attestation)
    empty = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert empty["status"] == "rejected"
    assert "attestation artifact is empty" in empty["exceptions"]


def test_result_artifact_must_bind_passed_case_set(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    result_path = tmp_path / candidate["artifacts"]["result"]["path"]
    result_path.write_text('{"status":"fail","cases":[]}')
    candidate["artifacts"]["result"]["sha256"] = sha256(result_path)
    result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "rejected"
    assert "result artifact does not match the submitted execution result" in result["exceptions"]


def test_untrusted_attestation_cannot_qualify(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["evidenceVerified"] is True
    assert result["status"] == "partial"
    assert "attestation is not analyst-trusted" in result["exceptions"]


def test_all_independence_dimensions_are_required(tmp_path: Path) -> None:
    for dimension in ("codebase", "oracle", "fixtureCuration"):
        candidate = packet(tmp_path)
        candidate["independence"][dimension] = "internal"
        result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
        assert result["status"] == "partial"
        assert result["qualifiesForV1"] is False


def test_release_candidate_freshness_boundary(tmp_path: Path) -> None:
    fresh = packet(tmp_path)
    fresh["maintenance"]["freshnessDate"] = "2026-04-16"
    fresh["execution"]["executedAt"] = "2026-04-16"
    assert classify_packet(fresh, evidence_root=tmp_path, today=dt.date(2026, 7, 15))["status"] == "qualifying"
    stale = copy.deepcopy(fresh)
    stale["maintenance"]["freshnessDate"] = "2026-04-15"
    result = classify_packet(stale, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "partial"
    assert "maintenance evidence is stale or future-dated" in result["exceptions"]


def test_complete_unique_passing_corpus_is_required(tmp_path: Path) -> None:
    for mutation in ("missing", "duplicate", "failed"):
        candidate = packet(tmp_path)
        if mutation == "missing":
            candidate["tests"].pop()
        elif mutation == "duplicate":
            candidate["tests"].append(candidate["tests"][0])
        else:
            candidate["tests"][0]["status"] = "fail"
        result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
        assert result["status"] != "qualifying"
        assert result["qualifiesForV1"] is False


def test_path_escape_and_missing_evidence_root_are_rejected(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["artifacts"]["source"]["path"] = "../source.tar"
    escaped = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert escaped["status"] == "rejected"
    no_root = classify(packet(tmp_path / "other"), today=dt.date(2026, 7, 15))
    assert no_root["status"] == "rejected"


def test_nonqualifying_outcomes_never_return_gate_success(tmp_path: Path) -> None:
    for outcome in ("partial", "conflicting", "withdrawn", "declined", "unresponsive"):
        candidate = packet(tmp_path)
        candidate["outcome"] = outcome
        result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
        assert result["status"] == outcome
        assert result["qualifiesForV1"] is False


def test_nonqualifying_outcome_cannot_mask_corrupt_evidence(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["outcome"] = "withdrawn"
    (tmp_path / candidate["artifacts"]["result"]["path"]).write_text("tampered")
    result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "rejected"


def test_contract_version_must_match_canonical_kit(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["contractVersions"] = ["pic-semantics/9.9.9"]
    result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "rejected"
    assert "contract versions do not match the canonical kit" in result["exceptions"]


def test_unresolved_mismatch_blocks_qualification(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["unresolvedMismatches"] = ["case differs from expected result"]
    result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "partial"
    assert "qualifying result has unresolved mismatches" in result["exceptions"]


def test_schema_rejects_mutable_revision_and_shell_command(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["sourceRevision"] = "main"
    candidate["execution"]["command"] = "python evaluate.py"
    result = classify_packet(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["schemaValid"] is False
    assert result["status"] == "rejected"


def test_non_object_packet_is_rejected_without_exception() -> None:
    for value in (None, [], "packet", 1):
        result = classify(value)
        assert result["status"] == "rejected"
        assert result["schemaValid"] is False
