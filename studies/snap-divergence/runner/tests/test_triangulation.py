from __future__ import annotations

import json
from pathlib import Path

from snap_divergence.triangulation import (
    EXCEPTION_REASONS,
    PROPOSED_DISPOSITIONS,
    SourceAssertion,
    load_fixture_cases,
    load_source_assertions,
    triangulate_divergence,
    triangulate_rows,
    write_triangulation_packet,
)


def _fixture(
    *,
    state: str = "GA",
    fixture_class: str = "gross_130_above",
    utility_surface: str = "standard",
    countable_assets: str = "200.00",
) -> dict:
    return {
        "caseId": "us-snap/fixture.test",
        "period": "2026-01",
        "entities": {
            "household": {
                "state": state,
                "fixtureClass": fixture_class,
                "utilitySurface": utility_surface,
            },
        },
        "inputs": {
            "us-snap/variable.countable_assets": {
                "value": countable_assets,
                "valueState": "known",
                "currency": "USD",
            },
        },
    }


def _comparison(*, pe_eligible: bool, prd_eligible: bool, difference: str = "100") -> dict:
    return {
        "caseId": "us-snap/fixture.test",
        "agreement": False,
        "classification": "state-option modeling",
        "decisionRelevant": True,
        "policyengine": {"eligible": pe_eligible, "allotment": "100"},
        "prd": {"eligible": prd_eligible, "allotment": "0"},
        "allotmentDifference": difference,
        "sourcePermalinks": ["https://example.invalid/engine"],
    }


def _assertion(
    topic: str,
    value: str | bool,
    *,
    jurisdiction: str = "GA",
    source_tier: str = "state_primary",
    retrieval_status: str = "verified",
    exception_reason: str | None = None,
    effective_start: str | None = "2025-10",
    effective_end: str | None = "2026-09",
    applies_to_topics: list[str] | None = None,
) -> SourceAssertion:
    return SourceAssertion(
        assertion_id=f"{jurisdiction}.{topic}",
        jurisdiction=jurisdiction,
        topic=topic,
        value=value,
        source_tier=source_tier,
        review_status="agent-proposed",
        retrieval_status=retrieval_status,
        source_url="https://example.invalid/source",
        effective_start=effective_start,
        effective_end=effective_end,
        exception_reason=exception_reason,
        applies_to_topics=applies_to_topics or [],
        source_refs=["https://example.invalid/source"],
        notes="test assertion",
    )


def _official_ga_assertions() -> list[SourceAssertion]:
    return [
        _assertion("bbce_status", True),
        _assertion("bbce_gross_limit_percent_fpl", "130"),
    ]


def test_triangulate_policyengine_bug_from_official_gross_source() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=True, prd_eligible=False),
        _fixture(),
        _official_ga_assertions(),
    )

    assert row["proposedDisposition"] == "confirmed_bug_policyengine"
    assert row["humanReviewRequired"] is False
    assert row["controllingAssertions"]


def test_triangulate_prd_bug_from_official_gross_source() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=False, prd_eligible=True),
        _fixture(),
        _official_ga_assertions(),
    )

    assert row["proposedDisposition"] == "confirmed_bug_prd"
    assert row["humanReviewRequired"] is False


def test_triangulate_expected_modeling_difference_when_eligibility_agrees() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=True, prd_eligible=True, difference="77.68"),
        _fixture(fixture_class="gross_130_below"),
        _official_ga_assertions(),
    )

    assert row["proposedDisposition"] == "expected_modeling_difference"
    assert row["exceptionReasons"] == []


def test_triangulate_fixture_adapter_issue_for_phone_only_utility() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=True, prd_eligible=True, difference="3.40"),
        _fixture(state="MS", fixture_class="utility_allowance_phone_only", utility_surface="standard"),
        [
            _assertion("bbce_status", False, jurisdiction="MS"),
            _assertion("phone_only_utility_allowance", "requires explicit phone-only input", jurisdiction="MS"),
        ],
    )

    assert row["proposedDisposition"] == "fixture_adapter_issue"
    assert row["humanReviewRequired"] is False


def test_triangulate_needs_review_for_blocked_official_source() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=True, prd_eligible=False),
        _fixture(state="TX"),
        [
            _assertion("bbce_status", True, jurisdiction="TX"),
            _assertion(
                "source_access",
                "blocked",
                jurisdiction="TX",
                retrieval_status="blocked",
                exception_reason="blocked official source",
                applies_to_topics=["bbce_gross_limit_percent_fpl"],
            ),
        ],
    )

    assert row["proposedDisposition"] == "needs_more_source_review"
    assert row["exceptionReasons"] == ["blocked official source"]
    assert row["humanReviewRequired"] is True


def test_triangulate_needs_review_for_conflicting_primary_sources() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=True, prd_eligible=False),
        _fixture(),
        [
            _assertion("bbce_status", True),
            _assertion("bbce_gross_limit_percent_fpl", "130"),
            _assertion("bbce_gross_limit_percent_fpl", "165"),
        ],
    )

    assert row["proposedDisposition"] == "needs_more_source_review"
    assert row["exceptionReasons"] == ["conflicting primary sources"]


def test_triangulate_needs_review_for_missing_effective_date() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=True, prd_eligible=False),
        _fixture(),
        [
            _assertion("bbce_status", True),
            _assertion("bbce_gross_limit_percent_fpl", "130", effective_start=None),
        ],
    )

    assert row["proposedDisposition"] == "needs_more_source_review"
    assert row["exceptionReasons"] == ["missing effective date"]


def test_triangulate_needs_review_for_secondary_only_evidence() -> None:
    row = triangulate_divergence(
        _comparison(pe_eligible=True, prd_eligible=False),
        _fixture(),
        [
            _assertion("bbce_status", True, source_tier="secondary"),
            _assertion("bbce_gross_limit_percent_fpl", "130", source_tier="secondary"),
        ],
    )

    assert row["proposedDisposition"] == "needs_more_source_review"
    assert row["exceptionReasons"] == ["secondary-source-only evidence"]


def test_triangulate_needs_review_for_underspecified_fixture() -> None:
    fixture = {"caseId": "us-snap/fixture.test", "period": "2026-01", "entities": {}, "inputs": {}}

    row = triangulate_divergence(_comparison(pe_eligible=True, prd_eligible=False), fixture, [])

    assert row["proposedDisposition"] == "needs_more_source_review"
    assert row["exceptionReasons"] == ["fixture assumption underspecified"]


def test_public_enums_cover_required_labels_and_exceptions() -> None:
    assert PROPOSED_DISPOSITIONS == {
        "confirmed_bug_policyengine",
        "confirmed_bug_prd",
        "expected_modeling_difference",
        "fixture_adapter_issue",
        "needs_more_source_review",
    }
    assert EXCEPTION_REASONS == {
        "blocked official source",
        "conflicting primary sources",
        "missing effective date",
        "fixture assumption underspecified",
        "secondary-source-only evidence",
    }


def test_current_held_divergences_receive_triaged_dispositions() -> None:
    assertions = load_source_assertions(Path("studies/snap-divergence/SOURCE_ASSERTIONS.json"))
    fixtures = load_fixture_cases(Path("studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json"))
    rows = [
        json.loads(line)
        for line in Path("studies/snap-divergence/results/classified-candidate-divergences.jsonl").read_text().splitlines()
        if line.strip()
    ]

    triangulated = triangulate_rows(rows, fixtures, assertions)
    divergent = [row for row in triangulated if not row.get("agreement")]
    counts: dict[str, int] = {}
    for row in divergent:
        counts[row["proposedDisposition"]] = counts.get(row["proposedDisposition"], 0) + 1

    assert len(divergent) == 15
    assert counts == {
        "confirmed_bug_policyengine": 5,
        "expected_modeling_difference": 2,
        "fixture_adapter_issue": 1,
        "needs_more_source_review": 7,
    }
    assert all(row["proposedDisposition"] != "confirmed_bug_prd" for row in divergent)


def test_write_triangulation_packet_contains_exception_queue(tmp_path) -> None:
    rows = [
        {
            "caseId": "us-snap/fixture.test",
            "agreement": False,
            "proposedDisposition": "needs_more_source_review",
            "exceptionReasons": ["blocked official source"],
            "humanReviewRequired": True,
            "dispositionDetail": "Blocked source.",
            "controllingAssertions": ["tx.source_access"],
        },
    ]
    path = tmp_path / "TRIANGULATED_ADJUDICATION_PACKET.md"

    write_triangulation_packet(path, rows)

    packet = path.read_text()
    assert "# SNAP Triangulated Adjudication Packet" in packet
    assert "| Human-review exceptions | 1 |" in packet
    assert "blocked official source" in packet
