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
    for name, content in {
        "source.tar": b"independent source",
        "input.json": b"{}\n",
        "result.json": json.dumps(
            {
                "status": "pass",
                "cases": [
                    item["path"]
                    for item in json.loads((KIT / "manifest.json").read_text())["artifacts"]
                    if item["role"] in {"valid", "invalid"}
                ],
            },
            sort_keys=True,
        ).encode(),
        "acknowledgement.txt": b"confirmed by external owner\n",
        "attestation.txt": b"external owner attestation\n",
    }.items():
        (evidence / name).write_bytes(content)
    manifest = json.loads((KIT / "manifest.json").read_text())
    cases = [item["path"] for item in manifest["artifacts"] if item["role"] in {"valid", "invalid"}]
    return {
        "schemaVersion": "rac-independent-submission.v2",
        "implementationId": "external-example",
        "organisation": {"name": "Example Org", "controlRelationship": "external"},
        "repository": {"url": "https://example.org/repo", "accessControl": "external"},
        "sourceRevision": "a" * 40,
        "contractVersions": ["pic-semantics/0.1.0"],
        "kitDigestSha256": kit_digest(),
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
                "acknowledgement": "acknowledgement.txt",
                "attestation": "attestation.txt",
            }.items()
        },
        "tests": [{"caseId": case, "status": "pass"} for case in cases],
        "outcome": "qualifying",
        "maintenance": {"owner": "Example Org", "freshnessDate": "2026-07-01"},
        "limitations": ["Structural conformance only"],
        "unresolvedMismatches": [],
    }


def test_artifact_backed_packet_qualifies(tmp_path: Path) -> None:
    result = classify(packet(tmp_path), evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["schemaValid"] is True
    assert result["evidenceVerified"] is True
    assert result["status"] == "qualifying"
    assert result["qualifiesForV1"] is True
    assert result["expiresAt"] == "2026-09-29"


def test_tampered_or_missing_artifact_fails_closed(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    (tmp_path / candidate["artifacts"]["result"]["path"]).write_text("tampered")
    result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "rejected"
    assert result["evidenceVerified"] is False
    assert any("result artifact digest mismatch" in item for item in result["exceptions"])


def test_artifact_roles_must_be_distinct_and_nonempty(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["artifacts"]["input"] = copy.deepcopy(candidate["artifacts"]["source"])
    aliased = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert aliased["status"] == "rejected"
    assert "artifact roles do not reference distinct paths" in aliased["exceptions"]

    candidate = packet(tmp_path)
    attestation = tmp_path / candidate["artifacts"]["attestation"]["path"]
    attestation.write_bytes(b"")
    candidate["artifacts"]["attestation"]["sha256"] = sha256(attestation)
    empty = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert empty["status"] == "rejected"
    assert "attestation artifact is empty" in empty["exceptions"]


def test_result_artifact_must_bind_passed_case_set(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    result_path = tmp_path / candidate["artifacts"]["result"]["path"]
    result_path.write_text('{"status":"fail","cases":[]}')
    candidate["artifacts"]["result"]["sha256"] = sha256(result_path)
    result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "rejected"
    assert "result artifact does not report a pass" in result["exceptions"]
    assert "result artifact case set does not match submission" in result["exceptions"]


def test_all_independence_dimensions_are_required(tmp_path: Path) -> None:
    for dimension in ("codebase", "oracle", "fixtureCuration"):
        candidate = packet(tmp_path)
        candidate["independence"][dimension] = "internal"
        result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
        assert result["status"] == "partial"
        assert result["qualifiesForV1"] is False


def test_release_candidate_freshness_boundary(tmp_path: Path) -> None:
    fresh = packet(tmp_path)
    fresh["maintenance"]["freshnessDate"] = "2026-04-16"
    fresh["execution"]["executedAt"] = "2026-04-16"
    assert classify(fresh, evidence_root=tmp_path, today=dt.date(2026, 7, 15))["status"] == "qualifying"
    stale = copy.deepcopy(fresh)
    stale["maintenance"]["freshnessDate"] = "2026-04-15"
    result = classify(stale, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
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
        result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
        assert result["status"] != "qualifying"
        assert result["qualifiesForV1"] is False


def test_path_escape_and_missing_evidence_root_are_rejected(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["artifacts"]["source"]["path"] = "../source.tar"
    escaped = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert escaped["status"] == "rejected"
    no_root = classify(packet(tmp_path / "other"), today=dt.date(2026, 7, 15))
    assert no_root["status"] == "rejected"


def test_nonqualifying_outcomes_never_return_gate_success(tmp_path: Path) -> None:
    for outcome in ("partial", "conflicting", "withdrawn", "declined", "unresponsive"):
        candidate = packet(tmp_path)
        candidate["outcome"] = outcome
        result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
        assert result["status"] == outcome
        assert result["qualifiesForV1"] is False


def test_unresolved_mismatch_blocks_qualification(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["unresolvedMismatches"] = ["case differs from expected result"]
    result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["status"] == "partial"
    assert "qualifying result has unresolved mismatches" in result["exceptions"]


def test_schema_rejects_mutable_revision_and_shell_command(tmp_path: Path) -> None:
    candidate = packet(tmp_path)
    candidate["sourceRevision"] = "main"
    candidate["execution"]["command"] = "python evaluate.py"
    result = classify(candidate, evidence_root=tmp_path, today=dt.date(2026, 7, 15))
    assert result["schemaValid"] is False
    assert result["status"] == "rejected"


def test_non_object_packet_is_rejected_without_exception() -> None:
    for value in (None, [], "packet", 1):
        result = classify(value)
        assert result["status"] == "rejected"
        assert result["schemaValid"] is False
