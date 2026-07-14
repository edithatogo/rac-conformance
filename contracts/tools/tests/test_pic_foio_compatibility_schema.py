import copy
import json

from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json, validator_for
from pic_contracts.validation import validate_file

BASE = CONTRACTS_ROOT / "pic-foio-compatibility" / "0.1.0" / "examples"


def test_valid_foio_compatibility_manifests_validate() -> None:
    validator = validator_for("pic-foio-compatibility")
    paths = sorted((BASE / "valid").glob("*.json"))
    assert len(paths) >= 2
    for path in paths:
        validator.validate(load_json(path))


def test_invalid_foio_compatibility_manifests_fail() -> None:
    validator = validator_for("pic-foio-compatibility")
    for path in sorted((BASE / "invalid").glob("*.json")):
        assert list(validator.iter_errors(load_json(path))), path.name


def test_wrapper_rejects_cross_jurisdiction_artifact(tmp_path) -> None:
    document = copy.deepcopy(load_json(BASE / "valid" / "nz-release.json"))
    document["picArtifacts"][0]["jurisdiction"] = "AU-NSW"
    path = tmp_path / "cross-jurisdiction.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    report = validate_file(path)
    assert not report.ok
    assert any(issue.code == "jurisdiction" for issue in report.issues)


def test_wrapper_rejects_time_and_evidence_drift(tmp_path) -> None:
    document = copy.deepcopy(load_json(BASE / "valid" / "nz-release.json"))
    document["picArtifacts"][1]["observedAt"] = "2026-07-15T00:00:00Z"
    document["picArtifacts"][2]["evidenceReferenceIds"] = ["missing"]
    path = tmp_path / "drift.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    report = validate_file(path)
    assert not report.ok
    assert {issue.code for issue in report.issues} == {"reference", "time"}


def test_generated_candidate_cannot_self_approve(tmp_path) -> None:
    document = copy.deepcopy(load_json(BASE / "valid" / "nz-release.json"))
    promotion = document["promotionRecords"][0]
    promotion["status"] = "approved"
    promotion["reviewer"] = "producing-agent"
    promotion["reviewEvidenceUri"] = "urn:sha256:" + "9" * 64
    path = tmp_path / "self-approved.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    errors = list(validator_for("pic-foio-compatibility").iter_errors(document))
    assert errors
    assert any("independentOfProducer" in list(error.absolute_path) for error in errors)


def test_gold_requires_approved_promotion_records(tmp_path) -> None:
    document = copy.deepcopy(load_json(BASE / "valid" / "nsw-release.json"))
    document["governance"].update(
        {
            "promotionState": "gold",
            "independentOracle": True,
            "reviewStatus": "approved",
        }
    )
    path = tmp_path / "unreviewed-gold.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    report = validate_file(path)
    assert not report.ok
    assert any(issue.code == "promotion" for issue in report.issues)
