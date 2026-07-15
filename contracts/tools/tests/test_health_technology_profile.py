"""Regression checks for health-technology authority boundaries."""

import json
from pathlib import Path

ROOT = Path(__file__).parents[3]
PROFILE = ROOT / "subrepos/process-mappings/profiles/health-technology"


def load_json(name: str) -> dict:
    return json.loads((PROFILE / name).read_text())


def test_authority_matrix_has_all_requested_authorities() -> None:
    matrix = load_json("AUTHORITY_MATRIX.json")
    authority_ids = {item["id"] for item in matrix["authorityCatalog"]}
    assert {
        "nz-medsafe",
        "nz-pharmac",
        "au-tga",
        "au-pbac",
        "au-pbs",
        "au-msac",
        "au-mbs",
        "uk-mhra",
        "uk-nice",
        "us-fda",
        "us-cms-medicare",
    } <= authority_ids


def test_matrix_rejects_false_equivalence() -> None:
    matrix = load_json("AUTHORITY_MATRIX.json")
    forbidden = {
        (rule["subject"], function)
        for rule in matrix["nonEquivalenceRules"]
        for function in rule["forbiddenFunctions"]
    }
    assert ("us-fda", "payer-coverage-determination") in forbidden
    assert ("au-mbs", "market-authorisation") in forbidden
    assert ("au-msac", "medicine-public-funding-and-listing") in forbidden
    assert ("au-pbac", "market-authorisation") in forbidden


def test_source_manifest_covers_matrix_sources_and_preserves_unavailable_states() -> None:
    matrix = load_json("AUTHORITY_MATRIX.json")
    manifest = load_json("sources/SOURCE_MANIFEST.json")
    source_ids = {item["id"] for item in manifest["sources"]}
    referenced = {
        source_id
        for function in matrix["functions"]
        for source_id in function["sourceIds"]
    }
    assert referenced <= source_ids
    assert "confidential-commercial-evidence" in manifest["unavailableEvidence"]
    assert all(item["sourceStatus"].startswith("official-") for item in manifest["sources"])
    assert all("effectiveFrom" in item and "supersededBy" in item for item in manifest["sources"])
    assert all(item["retrievalDigest"].startswith("sha256:") for item in manifest["sources"])


def test_money_and_outcomes_are_not_encoded_in_authority_matrix() -> None:
    matrix = load_json("AUTHORITY_MATRIX.json")
    serialized = json.dumps(matrix).lower()
    assert "clinical merit" in matrix["authorityBoundary"].lower()
    assert "price" in matrix["authorityBoundary"].lower()
    assert "recommendation" in serialized
    assert '"price":' not in serialized
    assert '"clinicalrecommendation":' not in serialized


def test_lifecycle_model_preserves_variation_and_loss_boundaries() -> None:
    model = (PROFILE / "LIFECYCLE_MODEL.md").read_text().lower()
    for term in ("parallel", "conditional", "terminated", "resubmitted", "representational loss"):
        assert term in model
    assert "fda is not a payer" in model
    assert "msac are not medicine regulators" in model
