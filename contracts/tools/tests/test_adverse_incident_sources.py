from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parents[3]
MANIFEST = (
    ROOT
    / "subrepos"
    / "process-mappings"
    / "profiles"
    / "adverse-incidents"
    / "sources"
    / "SOURCE_MANIFEST.json"
)
MATRIX = MANIFEST.parents[1] / "AUTHORITY_VARIATION_MATRIX.json"


def test_adverse_incident_source_ledger_has_expected_authority_layers() -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = {source["id"]: source for source in document["sources"]}

    assert set(sources) == {
        "nz-hqsc-national-adverse-events-policy-2023",
        "nz-hdc-code-consumers-rights",
        "au-open-disclosure-framework-2026",
        "au-nsqhs-action-1-12",
        "nsw-incident-management-pd2020-047",
        "nsw-open-disclosure-pd2023-034",
    }
    assert sources["nz-hdc-code-consumers-rights"]["authorityClass"] == "regulation"
    assert sources["au-open-disclosure-framework-2026"]["authorityClass"] == "national-framework"
    assert (
        sources["nsw-incident-management-pd2020-047"]["authorityClass"]
        == "state-policy-directive"
    )


def test_blocked_sources_are_explicit_and_not_filled_by_secondary_sources() -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert document["blockedSources"]
    for source in document["sources"]:
        expected_state = (
            "human-approved"
            if source["id"]
            in {
                "nz-hqsc-national-adverse-events-policy-2023",
                "nz-hdc-code-consumers-rights",
                "au-open-disclosure-framework-2026",
            }
            else "agent-proposed"
        )
        assert source["reviewerState"] == expected_state
        assert source["url"].startswith("https://")
        if source["id"] in document["blockedSources"]:
            assert source["sourceStatus"].endswith("download-blocked")
            assert source["digest"] is None


def test_authority_variation_matrix_does_not_create_a_false_crosswalk() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    source_ids = {source["id"] for source in manifest["sources"]}

    assert matrix["mappingState"] == "not-a-crosswalk"
    for layer in matrix["layers"]:
        assert set(layer["sourceIds"]).issubset(source_ids)
        assert "certified" not in layer["disposition"]
    assert {layer["id"] for layer in matrix["layers"]} >= {
        "national-consistency",
        "nz-consumer-rights",
        "australia-national-framework",
        "regional-implementation",
        "hypothetical-local-procedure",
    }
