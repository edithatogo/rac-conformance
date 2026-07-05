from __future__ import annotations

from decimal import Decimal

from snap_divergence.comparison import compare_pair, summarize_comparisons, write_report


def _result(case_id: str, eligible: bool, allotment: str) -> dict:
    return {
        "caseId": case_id,
        "outputs": {
            "us-snap/decision.eligible": {"value": eligible, "valueState": "known"},
            "us-snap/decision.allotment": {
                "value": allotment,
                "valueState": "known",
                "currency": "USD",
            },
        },
    }


def test_compare_pair_treats_one_dollar_as_agreement() -> None:
    comparison = compare_pair(
        _result("case.a", True, "100.00"),
        _result("case.a", True, "100.99"),
        tolerance=Decimal("1.00"),
    )

    assert comparison["agreement"] is True
    assert comparison["allotmentDifference"] == "0.99"
    assert comparison["classification"] == "agreement"


def test_compare_pair_marks_unclassified_decision_relevant_divergence() -> None:
    comparison = compare_pair(
        _result("case.b", True, "100.00"),
        _result("case.b", False, "80.00"),
        tolerance=Decimal("1.00"),
    )

    assert comparison["agreement"] is False
    assert comparison["classification"] == "unclassified"
    assert comparison["decisionRelevant"] is True
    assert comparison["evidence"]


def test_summarize_comparisons_counts_agreements() -> None:
    comparisons = [
        compare_pair(_result("a", True, "1"), _result("a", True, "1")),
        compare_pair(_result("b", True, "1"), _result("b", True, "3")),
    ]

    summary = summarize_comparisons(comparisons)

    assert summary == {
        "total": 2,
        "agreements": 1,
        "divergences": 1,
        "decisionRelevant": 0,
        "unclassified": 1,
    }


def test_write_report_contains_summary(tmp_path) -> None:
    comparisons = [
        compare_pair(_result("a", True, "1"), _result("a", True, "1")),
        compare_pair(_result("b", True, "1"), _result("b", True, "3")),
    ]
    path = tmp_path / "REPORT.md"

    write_report(path, comparisons)

    report = path.read_text()
    assert "# SNAP Divergence Draft Report" in report
    assert "| Total cases | 2 |" in report
    assert "| Divergences | 1 |" in report


def test_write_report_can_label_approved_fixtures(tmp_path) -> None:
    comparisons = [compare_pair(_result("a", True, "1"), _result("a", True, "1"))]
    path = tmp_path / "APPROVED.md"

    write_report(path, comparisons, fixture_label="approved fixtures", evidence_label="approved")

    report = path.read_text()
    assert "generated from approved fixtures" in report
    assert "policyengine-approved-results.jsonl" in report
    assert "comparison-approved-results.jsonl" in report
