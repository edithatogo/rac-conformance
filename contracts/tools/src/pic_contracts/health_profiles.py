"""Candidate-only health-technology profile safety rules."""

from __future__ import annotations

from typing import Any


def validate_candidate_document(document: dict[str, Any]) -> list[str]:
    """Validate non-schema safety boundaries for a candidate profile."""
    errors: list[str] = []
    if not document.get("profileId", "").startswith("health-technology/process."):
        errors.append("candidate profile must use the health-technology process namespace")
    for assertion in document.get("sourceAssertions", []):
        if assertion.get("controlling") and not (
            assertion.get("sourceType") == "official_primary"
            and assertion.get("reviewStatus") in {"official-primary", "human-approved"}
        ):
            errors.append(
                "controlling source assertion is not independently eligible: "
                f"{assertion.get('id')}"
            )
    if any(trace.get("equivalenceClaim") != "none" for trace in document.get("traces", [])):
        errors.append("candidate traces must not claim equivalence")
    if not any(
        item.get("kind") == "human_adjudication_required"
        for item in document.get("exceptions", [])
    ):
        errors.append("candidate profile must retain a human adjudication exception")
    return errors
