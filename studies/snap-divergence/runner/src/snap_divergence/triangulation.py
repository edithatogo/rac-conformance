"""Deterministic source triangulation for held SNAP divergences."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from snap_divergence.comparison import load_jsonl

DEFAULT_CLASSIFIED_RESULTS = Path("studies/snap-divergence/results/classified-candidate-divergences.jsonl")
DEFAULT_FIXTURES = Path("studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json")
DEFAULT_SOURCE_ASSERTIONS = Path("studies/snap-divergence/SOURCE_ASSERTIONS.json")
DEFAULT_TRIANGULATED_RESULTS = Path("studies/snap-divergence/results/triangulated-candidate-divergences.jsonl")
DEFAULT_PACKET = Path("studies/snap-divergence/TRIANGULATED_ADJUDICATION_PACKET.md")

PROPOSED_DISPOSITIONS = {
    "confirmed_bug_policyengine",
    "confirmed_bug_prd",
    "expected_modeling_difference",
    "fixture_adapter_issue",
    "needs_more_source_review",
}

EXCEPTION_REASONS = {
    "blocked official source",
    "conflicting primary sources",
    "missing effective date",
    "fixture assumption underspecified",
    "secondary-source-only evidence",
}

OFFICIAL_SOURCE_TIERS = {
    "federal_primary",
    "federal_official_state_option",
    "state_primary",
    "state_official",
}

PRIORITIZED_EXCEPTIONS = [
    "blocked official source",
    "conflicting primary sources",
    "missing effective date",
    "fixture assumption underspecified",
    "secondary-source-only evidence",
]


@dataclass(frozen=True)
class SourceAssertion:
    assertion_id: str
    jurisdiction: str
    topic: str
    value: str | bool | None
    source_tier: str
    review_status: str
    retrieval_status: str
    source_url: str
    effective_start: str | None = None
    effective_end: str | None = None
    exception_reason: str | None = None
    applies_to_topics: list[str] | None = None
    source_refs: list[str] | None = None
    notes: str = ""

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any], source_refs: list[str] | None = None) -> SourceAssertion:
        return cls(
            assertion_id=mapping["assertionId"],
            jurisdiction=mapping["jurisdiction"],
            topic=mapping["topic"],
            value=mapping.get("value"),
            source_tier=mapping["sourceTier"],
            review_status=mapping.get("reviewStatus", "agent-proposed"),
            retrieval_status=mapping.get("retrievalStatus", "verified"),
            source_url=mapping.get("sourceUrl", ""),
            effective_start=mapping.get("effectiveStart"),
            effective_end=mapping.get("effectiveEnd"),
            exception_reason=mapping.get("exceptionReason"),
            applies_to_topics=list(mapping.get("appliesToTopics", [])),
            source_refs=list(source_refs or mapping.get("sourceRefs", [])),
            notes=mapping.get("notes", ""),
        )

    @property
    def is_controlling(self) -> bool:
        return self.review_status == "human-approved" or self.source_tier in OFFICIAL_SOURCE_TIERS

    @property
    def is_blocked(self) -> bool:
        return self.retrieval_status == "blocked"


def load_source_assertions(path: Path) -> list[SourceAssertion]:
    doc = json.loads(path.read_text())
    if "assertions" in doc:
        return [SourceAssertion.from_mapping(assertion) for assertion in doc["assertions"]]
    assertions: list[SourceAssertion] = []
    for case in doc.get("cases", []):
        assertion = case.get("entities", {}).get("sourceAssertion")
        if assertion:
            assertions.append(SourceAssertion.from_mapping(assertion, case.get("sourceRefs", [])))
    return assertions


def load_fixture_cases(path: Path) -> dict[str, dict[str, Any]]:
    doc = json.loads(path.read_text())
    return {case["caseId"]: case for case in doc.get("cases", [])}


def triangulate_rows(
    rows: list[dict[str, Any]],
    fixtures: dict[str, dict[str, Any]],
    assertions: list[SourceAssertion],
) -> list[dict[str, Any]]:
    return [
        triangulate_divergence(row, fixtures.get(row["caseId"], {}), assertions)
        for row in rows
        if not row.get("agreement")
    ]


def triangulate_divergence(
    comparison: dict[str, Any],
    fixture: dict[str, Any],
    assertions: list[SourceAssertion],
) -> dict[str, Any]:
    result = dict(comparison)
    context = _fixture_context(fixture)
    if not context:
        return _with_exception(result, ["fixture assumption underspecified"], [], "Fixture is missing state, period, or fixture-class metadata required for deterministic source resolution.")

    state, fixture_class, utility_surface, period = context
    relevant_topics = _relevant_topics(fixture_class, utility_surface, comparison.get("classification", ""))
    applicable = _applicable_assertions(assertions, state, relevant_topics, period)
    controlling = [assertion for assertion in applicable if assertion.is_controlling and not assertion.is_blocked]
    exception_reasons = _exception_reasons(applicable, controlling, relevant_topics)
    if exception_reasons:
        return _with_exception(
            result,
            exception_reasons,
            applicable,
            "Human source review is required before a deterministic bug or modeling disposition can be emitted.",
        )

    expected_eligibility = _expected_eligibility(fixture, controlling)
    if expected_eligibility is not None:
        policyengine_eligible = bool(comparison.get("policyengine", {}).get("eligible"))
        prd_eligible = bool(comparison.get("prd", {}).get("eligible"))
        if policyengine_eligible != prd_eligible:
            if policyengine_eligible == expected_eligibility and prd_eligible != expected_eligibility:
                return _with_disposition(
                    result,
                    "confirmed_bug_prd",
                    controlling,
                    "Official source assertions resolve expected eligibility and PolicyEngine matches that source-derived result while PRD does not.",
                )
            if prd_eligible == expected_eligibility and policyengine_eligible != expected_eligibility:
                return _with_disposition(
                    result,
                    "confirmed_bug_policyengine",
                    controlling,
                    "Official source assertions resolve expected eligibility and PRD matches that source-derived result while PolicyEngine does not.",
                )

    if fixture_class == "utility_allowance_phone_only":
        return _with_disposition(
            result,
            "fixture_adapter_issue",
            controlling,
            "The held divergence is non-decision-relevant and turns on whether the fixture encodes phone-only, generic utilities, or heating/cooling responsibility for both engines.",
        )

    if _engines_agree_on_eligibility(comparison):
        return _with_disposition(
            result,
            "expected_modeling_difference",
            controlling,
            "Official source assertions resolve the eligibility surface, but the remaining mismatch is an allotment-only engine modeling or parameter-surface difference.",
        )

    return _with_exception(
        result,
        ["fixture assumption underspecified"],
        controlling,
        "The fixture and source assertions do not determine which engine should control this divergence.",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def write_triangulation_packet(path: Path, rows: list[dict[str, Any]]) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        disposition = row["proposedDisposition"]
        counts[disposition] = counts.get(disposition, 0) + 1
    human_review = [row for row in rows if row.get("humanReviewRequired")]
    lines = [
        "# SNAP Triangulated Adjudication Packet",
        "",
        "This packet is generated by the deterministic source triangulation resolver. It proposes dispositions from source assertions, fixture assumptions, and engine outputs; it is not an upstream issue submission.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Held divergences | {len(rows)} |",
        f"| Human-review exceptions | {len(human_review)} |",
    ]
    for disposition in sorted(counts):
        lines.append(f"| {disposition} | {counts[disposition]} |")
    lines.extend(
        [
            "",
            "## Human Review Queue",
            "",
        ],
    )
    if human_review:
        lines.extend(["| Case | Proposed disposition | Exception reasons |", "|---|---|---|"])
        for row in human_review:
            reasons = ", ".join(row.get("exceptionReasons", []))
            lines.append(f"| `{row['caseId']}` | {row['proposedDisposition']} | {reasons} |")
    else:
        lines.append("No cases require human review under the current source assertions.")
    lines.extend(
        [
            "",
            "## Proposed Dispositions",
            "",
            "| Case | Disposition | Human review | Detail |",
            "|---|---|---|---|",
        ],
    )
    for row in rows:
        lines.append(
            f"| `{row['caseId']}` | {row['proposedDisposition']} | "
            f"{str(row.get('humanReviewRequired', False)).lower()} | {row['dispositionDetail']} |",
        )
    lines.extend(["", "## Controlling Assertions", ""])
    for row in rows:
        lines.append(f"### `{row['caseId']}`")
        lines.append("")
        for assertion_id in row.get("controllingAssertions", []):
            lines.append(f"- `{assertion_id}`")
        if not row.get("controllingAssertions"):
            lines.append("- None")
        lines.append("")
    path.write_text("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classified", type=Path, default=DEFAULT_CLASSIFIED_RESULTS)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--source-assertions", type=Path, default=DEFAULT_SOURCE_ASSERTIONS)
    parser.add_argument("--output", type=Path, default=DEFAULT_TRIANGULATED_RESULTS)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    args = parser.parse_args(argv)

    assertions = load_source_assertions(args.source_assertions)
    fixtures = load_fixture_cases(args.fixtures)
    triangulated = triangulate_rows(load_jsonl(args.classified), fixtures, assertions)
    write_jsonl(args.output, triangulated)
    write_triangulation_packet(args.packet, triangulated)
    return 0


def _fixture_context(fixture: dict[str, Any]) -> tuple[str, str, str, str] | None:
    household = fixture.get("entities", {}).get("household", {})
    state = household.get("state")
    fixture_class = household.get("fixtureClass")
    period = fixture.get("period")
    if not state or not fixture_class or not period:
        return None
    return state, fixture_class, household.get("utilitySurface", ""), period


def _relevant_topics(fixture_class: str, utility_surface: str, classification: str) -> set[str]:
    topics: set[str] = set()
    if fixture_class in {"bbce_165_boundary", "gross_130_above", "gross_130_below"}:
        topics.update({"bbce_status", "bbce_gross_limit_percent_fpl"})
    if fixture_class == "asset_above_limit":
        topics.update({"bbce_status", "asset_limit_usd"})
    if fixture_class == "utility_allowance_phone_only":
        topics.add("phone_only_utility_allowance")
    if utility_surface == "heat_and_eat" or classification == "deduction handling":
        topics.add("utility_allowance_exact_value")
    return topics


def _applicable_assertions(
    assertions: list[SourceAssertion],
    state: str,
    relevant_topics: set[str],
    period: str,
) -> list[SourceAssertion]:
    applicable = []
    for assertion in assertions:
        if assertion.jurisdiction not in {state, "US"}:
            continue
        if not _assertion_topic_applies(assertion, relevant_topics):
            continue
        if assertion.is_blocked or _covers_period(assertion, period):
            applicable.append(assertion)
    return applicable


def _assertion_topic_applies(assertion: SourceAssertion, relevant_topics: set[str]) -> bool:
    if assertion.topic in relevant_topics:
        return True
    if assertion.applies_to_topics and set(assertion.applies_to_topics) & relevant_topics:
        return True
    return assertion.topic == "source_access" and bool(set(assertion.applies_to_topics or []) & relevant_topics)


def _covers_period(assertion: SourceAssertion, period: str) -> bool:
    if assertion.effective_start is None or assertion.effective_end is None:
        return True
    period_month = period[:7]
    return assertion.effective_start <= period_month <= assertion.effective_end


def _exception_reasons(
    applicable: list[SourceAssertion],
    controlling: list[SourceAssertion],
    relevant_topics: set[str],
) -> list[str]:
    reasons: set[str] = set()
    if any(assertion.is_blocked for assertion in applicable):
        reasons.add("blocked official source")
    if _has_primary_conflict(controlling):
        reasons.add("conflicting primary sources")
    if any(
        assertion.topic in relevant_topics
        and assertion.is_controlling
        and assertion.retrieval_status == "verified"
        and (assertion.effective_start is None or assertion.effective_end is None)
        for assertion in applicable
    ):
        reasons.add("missing effective date")
    if not reasons and relevant_topics and not controlling and applicable:
        reasons.add("secondary-source-only evidence")
    if not reasons and relevant_topics and not applicable:
        reasons.add("secondary-source-only evidence")
    return [reason for reason in PRIORITIZED_EXCEPTIONS if reason in reasons]


def _has_primary_conflict(assertions: list[SourceAssertion]) -> bool:
    values_by_topic: dict[str, set[str]] = {}
    for assertion in assertions:
        if assertion.value is None:
            continue
        values_by_topic.setdefault(assertion.topic, set()).add(str(assertion.value))
    return any(len(values) > 1 for values in values_by_topic.values())


def _expected_eligibility(fixture: dict[str, Any], assertions: list[SourceAssertion]) -> bool | None:
    household = fixture.get("entities", {}).get("household", {})
    fixture_class = household.get("fixtureClass")
    values = _values_by_topic(assertions)
    if fixture_class == "asset_above_limit":
        asset_limit = _decimal(values.get("asset_limit_usd"))
        countable_assets = _decimal(
            fixture.get("inputs", {}).get("us-snap/variable.countable_assets", {}).get("value"),
        )
        if asset_limit is not None and countable_assets is not None:
            return countable_assets <= asset_limit
    if fixture_class == "bbce_165_boundary":
        if values.get("bbce_status") is False:
            return False
        gross_limit = _decimal(values.get("bbce_gross_limit_percent_fpl"))
        if gross_limit is not None:
            return gross_limit >= Decimal("165")
    if fixture_class == "gross_130_above":
        if values.get("bbce_status") is False:
            return False
        gross_limit = _decimal(values.get("bbce_gross_limit_percent_fpl"))
        if gross_limit is not None:
            return gross_limit > Decimal("130")
    if fixture_class == "gross_130_below":
        return True
    return None


def _values_by_topic(assertions: list[SourceAssertion]) -> dict[str, str | bool | None]:
    values: dict[str, str | bool | None] = {}
    for assertion in assertions:
        values.setdefault(assertion.topic, assertion.value)
    return values


def _decimal(value: str | bool | None) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def _engines_agree_on_eligibility(comparison: dict[str, Any]) -> bool:
    return bool(comparison.get("policyengine", {}).get("eligible")) == bool(comparison.get("prd", {}).get("eligible"))


def _with_disposition(
    row: dict[str, Any],
    disposition: str,
    controlling: list[SourceAssertion],
    detail: str,
) -> dict[str, Any]:
    row["proposedDisposition"] = disposition
    row["dispositionDetail"] = detail
    row["exceptionReasons"] = []
    row["humanReviewRequired"] = False
    row["controllingAssertions"] = [assertion.assertion_id for assertion in controlling]
    row["controllingSourceRefs"] = _source_refs(controlling)
    return row


def _with_exception(
    row: dict[str, Any],
    reasons: list[str],
    assertions: list[SourceAssertion],
    detail: str,
) -> dict[str, Any]:
    row["proposedDisposition"] = "needs_more_source_review"
    row["dispositionDetail"] = detail
    row["exceptionReasons"] = reasons
    row["humanReviewRequired"] = True
    row["controllingAssertions"] = [assertion.assertion_id for assertion in assertions]
    row["controllingSourceRefs"] = _source_refs(assertions)
    return row


def _source_refs(assertions: list[SourceAssertion]) -> list[str]:
    refs: list[str] = []
    for assertion in assertions:
        refs.extend(assertion.source_refs or [assertion.source_url])
    return list(dict.fromkeys(ref for ref in refs if ref))


if __name__ == "__main__":
    raise SystemExit(main())
