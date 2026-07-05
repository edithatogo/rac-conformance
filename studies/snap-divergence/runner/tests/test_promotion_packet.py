from pathlib import Path

from snap_divergence.promotion_packet import (
    build_promoted_fixture_file,
    build_promotion_rows,
    summarize_rows,
    write_packet,
)


def test_build_promotion_rows_recommends_agreements_only() -> None:
    candidates = {
        "case.a": {
            "caseId": "case.a",
            "description": "agreement",
            "entities": {"household": {"state": "CA", "fixtureClass": "baseline"}},
        },
        "case.b": {
            "caseId": "case.b",
            "description": "divergence",
            "entities": {"household": {"state": "TX", "fixtureClass": "asset"}},
        },
    }
    comparisons = [
        _comparison("case.a", agreement=True, decision_relevant=False),
        _comparison("case.b", agreement=False, decision_relevant=True),
    ]

    rows = build_promotion_rows(candidates, comparisons)

    assert rows[0]["recommendation"] == "promote"
    assert rows[1]["recommendation"] == "hold"
    assert summarize_rows(rows) == {
        "total": 2,
        "recommended": 1,
        "held": 1,
        "decisionRelevantHeld": 1,
    }


def test_write_packet_separates_recommended_and_held(tmp_path: Path) -> None:
    rows = [
        _row("case.a", recommendation="promote", decision_relevant=False),
        _row("case.b", recommendation="hold", decision_relevant=True),
    ]
    output = tmp_path / "packet.md"

    write_packet(output, rows)

    text = output.read_text()
    assert "| Recommended for promotion | 1 |" in text
    assert "| Held for divergence analysis | 1 |" in text
    assert "## Recommended Promotion Cases" in text
    assert "`case.a`" in text
    assert "## Held Cases" in text
    assert "`case.b`" in text


def test_build_promoted_fixture_file_keeps_only_agreements() -> None:
    candidate_file = {
        "conformsTo": "pic-fixtures/0.1.0",
        "cases": [
            {
                "caseId": "case.a",
                "description": "agreement",
                "period": "2026-01",
                "entities": {},
                "inputs": {},
                "expected": {"old": {"valueState": "unknown"}},
                "sourceRefs": ["source"],
            },
            {
                "caseId": "case.b",
                "description": "divergence",
                "period": "2026-01",
                "entities": {},
                "inputs": {},
                "expected": {"old": {"valueState": "unknown"}},
                "sourceRefs": ["source"],
            },
        ],
    }

    promoted = build_promoted_fixture_file(
        candidate_file,
        [
            _comparison("case.a", agreement=True, decision_relevant=False),
            _comparison("case.b", agreement=False, decision_relevant=True),
        ],
    )

    assert promoted["provenance"]["method"] == "human"
    assert [case["caseId"] for case in promoted["cases"]] == ["case.a"]
    expected = promoted["cases"][0]["expected"]
    assert expected["us-snap/decision.eligible"]["value"] is True
    assert expected["us-snap/decision.allotment"] == {
        "value": "100",
        "valueState": "known",
        "epistemicStatus": "observed",
        "currency": "USD",
        "tolerance": "1",
    }
    assert promoted["cases"][0]["provenance"]["method"] == "human"


def _comparison(case_id: str, *, agreement: bool, decision_relevant: bool) -> dict:
    return {
        "caseId": case_id,
        "agreement": agreement,
        "classification": "agreement" if agreement else "state-option modeling",
        "decisionRelevant": decision_relevant,
        "policyengine": {"eligible": True, "allotment": "100"},
        "prd": {"eligible": True, "allotment": "100" if agreement else "0"},
        "allotmentDifference": "0" if agreement else "100",
        "tolerance": "1",
    }


def _row(case_id: str, *, recommendation: str, decision_relevant: bool) -> dict:
    return {
        "caseId": case_id,
        "state": "CA",
        "fixtureClass": "baseline",
        "recommendation": recommendation,
        "classification": "agreement" if recommendation == "promote" else "state-option modeling",
        "decisionRelevant": decision_relevant,
        "policyengineEligible": True,
        "policyengineAllotment": "100",
        "prdEligible": True,
        "prdAllotment": "100" if recommendation == "promote" else "0",
        "allotmentDifference": "0" if recommendation == "promote" else "100",
    }
