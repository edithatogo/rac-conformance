from __future__ import annotations

import json
from pathlib import Path

from pic_contracts.health_profiles import validate_candidate_document
from pic_contracts.process_profile import normalize_trace
from pic_contracts.validation import validate_file

ROOT = Path(__file__).parents[3] / "subrepos/process-mappings/profiles/health-technology"
PROFILES = (
    ROOT / "candidates/nz-pembrolizumab-pathway.json",
    ROOT / "candidates/uk-pembrolizumab-pathway.json",
)


def test_candidate_profiles_validate_without_controlling_assertions() -> None:
    for path in PROFILES:
        document = json.loads(path.read_text(encoding="utf-8"))
        report = validate_file(path)
        assert report.ok, report.to_dict()
        assert validate_candidate_document(document) == []
        assert all(not assertion["controlling"] for assertion in document["sourceAssertions"])
        assert all(
            assertion["reviewStatus"] == "agent-proposed"
            for assertion in document["sourceAssertions"]
        )
        assert document["traces"][0]["equivalenceClaim"] == "none"


def test_candidate_profiles_have_distinct_jurisdiction_and_authority_paths() -> None:
    nz = json.loads(PROFILES[0].read_text(encoding="utf-8"))
    uk = json.loads(PROFILES[1].read_text(encoding="utf-8"))
    assert nz["jurisdiction"] == "NZ"
    assert uk["jurisdiction"] == "UK"
    assert {event["actorId"] for event in nz["events"]} != {
        event["actorId"] for event in uk["events"]
    }
    assert any("Medsafe" in actor["name"] for actor in nz["actors"])
    assert any("MHRA" in actor["name"] for actor in uk["actors"])


def test_candidate_trace_normalization_is_deterministic() -> None:
    for path in PROFILES:
        document = json.loads(path.read_text(encoding="utf-8"))
        trace_id = document["traces"][0]["id"]
        assert normalize_trace(document, trace_id) == normalize_trace(document, trace_id)


def test_candidate_profile_rejects_controlling_agent_assertion() -> None:
    document = json.loads(PROFILES[0].read_text(encoding="utf-8"))
    document["sourceAssertions"][0]["controlling"] = True
    assert validate_candidate_document(document) == [
        "controlling source assertion is not independently eligible: "
        "health/source/nz-medsafe-evaluation"
    ]


def test_candidate_profile_rejects_non_none_trace_equivalence() -> None:
    document = json.loads(PROFILES[1].read_text(encoding="utf-8"))
    document["traces"][0]["equivalenceClaim"] = "path"
    assert validate_candidate_document(document) == ["candidate traces must not claim equivalence"]


def test_candidate_boundary_handles_missing_optional_fields() -> None:
    assert validate_candidate_document({}) == [
        "candidate profile must use the health-technology process namespace",
        "candidate profile must retain a human adjudication exception",
    ]
