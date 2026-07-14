from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
BASE = ROOT / "subrepos/process-mappings/profiles/adverse-incidents/candidates"
MODULE_PATH = ROOT / "tools/adverse_incident_triangulation.py"
MODULE_SPEC = importlib.util.spec_from_file_location(
    "adverse_incident_triangulation", MODULE_PATH
)
assert MODULE_SPEC and MODULE_SPEC.loader
MODULE = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = MODULE
MODULE_SPEC.loader.exec_module(MODULE)
resolve = MODULE.resolve


def test_candidate_resolver_is_data_driven_and_covers_all_labels() -> None:
    results = resolve(BASE / "SOURCE_ASSERTIONS.json", BASE / "CANDIDATE_MAPPINGS.json")
    by_id = {result.mapping_id: result for result in results}

    assert len(results) == 6
    assert by_id["mapping.nz.consumer-informed"].label == "candidate_supported"
    assert by_id["mapping.au.open-disclosure"].label == "needs_more_source_review"
    assert by_id["mapping.nsw.incident-review"].label == "needs_more_source_review"
    assert by_id["mapping.nsw.incident-review"].exception_reasons == (
        "blocked official source",
    )
    assert by_id["mapping.local.escalation"].label == "needs_more_source_review"
    assert by_id["mapping.local.escalation"].exception_reasons == (
        "fixture assumption underspecified",
    )
    assert by_id["mapping.au.secondary-summary"].label == "needs_more_source_review"
    assert by_id["mapping.au.secondary-summary"].exception_reasons == (
        "secondary-source-only evidence",
    )
    assert all(result.human_review_required for result in results)
    assert all("confirmed" not in result.label for result in results)


def test_candidate_corpus_remains_agent_proposed() -> None:
    document = json.loads((BASE / "CANDIDATE_MAPPINGS.json").read_text(encoding="utf-8"))

    assert document["method"] == "agent-proposed"
    assert document["reviewState"] == "candidate"
    assert all(
        mapping["loss"] and mapping["humanTasks"]
        for mapping in document["mappings"]
        if mapping["id"] != "mapping.au.secondary-summary"
    )


def test_jurisdictional_overlay_is_expected_difference_when_source_is_current(tmp_path) -> None:
    assertions = {
        "assertions": [
            {
                "id": "a1",
                "jurisdiction": "NZ",
                "sourceStatus": "current",
                "effectiveDateStatus": "verified",
                "authorityClass": "regulation",
            }
        ]
    }
    mappings = {
        "mappings": [
            {
                "id": "m1",
                "jurisdiction": "NZ",
                "kind": "jurisdictional-overlay",
                "sourceAssertionIds": ["a1"],
            }
        ]
    }
    assertions_path = tmp_path / "assertions.json"
    mappings_path = tmp_path / "mappings.json"
    assertions_path.write_text(json.dumps(assertions), encoding="utf-8")
    mappings_path.write_text(json.dumps(mappings), encoding="utf-8")

    result = resolve(assertions_path, mappings_path)[0]

    assert result.label == "expected_jurisdictional_difference"
    assert result.exception_reasons == ()


def test_jurisdiction_and_effective_date_leakage_becomes_exception(tmp_path) -> None:
    assertions_path = tmp_path / "assertions.json"
    mappings_path = tmp_path / "mappings.json"
    assertions_path.write_text(
        json.dumps(
            {
                "assertions": [
                    {
                        "id": "a1",
                        "jurisdiction": "NZ",
                        "sourceStatus": "current",
                        "effectiveDateStatus": "not-stated",
                        "authorityClass": "regulation",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    mappings_path.write_text(
        json.dumps(
            {
                "mappings": [
                    {
                        "id": "m1",
                        "jurisdiction": "AU",
                        "kind": "consumer-communication",
                        "sourceAssertionIds": ["a1"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = resolve(assertions_path, mappings_path)[0]

    assert result.label == "needs_more_source_review"
    assert result.exception_reasons == (
        "conflicting jurisdictional authority",
        "missing effective date",
    )


def test_generated_result_has_one_disposition_per_candidate(tmp_path) -> None:
    output_path = tmp_path / "triangulated.json"
    MODULE.write_results(
        BASE / "SOURCE_ASSERTIONS.json",
        BASE / "CANDIDATE_MAPPINGS.json",
        output_path,
    )

    document = json.loads(output_path.read_text(encoding="utf-8"))

    assert document["method"] == "deterministic-source-triangulation"
    assert len(document["results"]) == 6
    assert {result["mappingId"] for result in document["results"]} == {
        "mapping.nz.consumer-informed",
        "mapping.nz.review-learning",
        "mapping.au.open-disclosure",
        "mapping.nsw.incident-review",
        "mapping.au.secondary-summary",
        "mapping.local.escalation",
    }
