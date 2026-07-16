"""Generate synthetic adverse-incident process-profile candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCENARIOS = (
    ("harm", "nz-hdc-code-consumers-rights", "NZ", "regulation", "1996-07-01"),
    (
        "near-miss",
        "nz-hqsc-national-adverse-events-policy-2023",
        "NZ",
        "national_policy",
        "2023-07-01",
    ),
    (
        "delayed-recognition",
        "au-open-disclosure-framework-2026",
        "AU",
        "guidance",
        "2026-06-25",
    ),
    (
        "disputed-facts",
        "nsw-incident-management-pd2020-047",
        "AU-NSW",
        "regional_policy",
        "2020-12-14",
    ),
    (
        "parallel-complaint",
        "nsw-open-disclosure-pd2023-034",
        "AU-NSW",
        "regional_policy",
        "2023-10-18",
    ),
    (
        "blocked-source",
        "nz-hqsc-national-adverse-events-policy-2023",
        "NZ",
        "national_policy",
        "2023-07-01",
    ),
)

SOURCE_REFS = {
    "nz-hdc-code-consumers-rights": "https://www.hdc.org.nz/your-rights/about-the-code/code-of-health-and-disability-services-consumers-rights/",
    "nz-hqsc-national-adverse-events-policy-2023": "https://www.hqsc.govt.nz/resources/resource-library/national-adverse-event-policy-2023/",
    "au-open-disclosure-framework-2026": "https://www.safetyandquality.gov.au/resources/australian-open-disclosure-framework-better-communication-better-care",
    "nsw-incident-management-pd2020-047": "https://www1.health.nsw.gov.au/pds/Pages/doc.aspx?dn=PD2020_047",
    "nsw-open-disclosure-pd2023-034": "https://www1.health.nsw.gov.au/pds/Pages/doc.aspx?dn=PD2023_034",
}


def build_profile(scenario: tuple[str, str, str, str, str]) -> dict[str, object]:
    name, source_id, jurisdiction, authority_class, effective_from = scenario
    prefix = f"adverse-incidents/{name}"
    actor_id = f"adverse-incidents/{name}/synthetic-reviewer"
    source_id_ref = f"adverse-incidents/{name}/source/{source_id}"
    source_assertion = (
        "The official source was unavailable to the agent and requires human review."
        if name == "blocked-source"
        else "Synthetic fixture assertion proposed for schema and harness testing."
    )
    profile: dict[str, object] = {
        "conformsTo": "pic-process-profile/0.1.0",
        "profileId": prefix,
        "profileVersion": "0.1.0",
        "processDefinitionVersion": "0.1.0",
        "jurisdiction": jurisdiction,
        "applicableAt": f"{effective_from}T00:00:00Z",
        "observedAt": "2026-07-03T00:00:00Z",
        "states": [
            {"id": f"{prefix}/state/detected", "kind": "initial", "label": "Incident detected", "sourceAssertionIds": [source_id_ref]},
            {"id": f"{prefix}/state/review", "kind": "intermediate", "label": "Human review", "sourceAssertionIds": [source_id_ref]},
            {"id": f"{prefix}/state/closed", "kind": "terminal", "label": "Review closed", "sourceAssertionIds": [source_id_ref]},
        ],
        "events": [
            {
                "id": f"{prefix}/event/detected",
                "kind": "observed_event",
                "eventType": "IncidentDetected",
                "occurredAt": "2026-07-01T00:00:00Z",
                "observedAt": "2026-07-01T00:00:00Z",
                "actorId": actor_id,
                "sourceAssertionIds": [source_id_ref],
            },
            {
                "id": f"{prefix}/event/review-closed",
                "kind": "certified_human_decision",
                "eventType": "ReviewClosed",
                "occurredAt": "2026-07-03T00:00:00Z",
                "observedAt": "2026-07-03T00:00:00Z",
                "actorId": actor_id,
                "sourceAssertionIds": [source_id_ref],
            },
        ],
        "transitions": [
            {
                "id": f"{prefix}/transition/review",
                "fromStateId": f"{prefix}/state/detected",
                "toStateId": f"{prefix}/state/review",
                "triggerEventId": f"{prefix}/event/detected",
                "sourceAssertionIds": [source_id_ref],
            },
            {
                "id": f"{prefix}/transition/closed",
                "fromStateId": f"{prefix}/state/review",
                "toStateId": f"{prefix}/state/closed",
                "triggerEventId": f"{prefix}/event/review-closed",
                "sourceAssertionIds": [source_id_ref],
            },
        ],
        "actors": [{"id": actor_id, "kind": "person", "name": "Synthetic human reviewer"}],
        "tasks": [
            {
                "id": f"{prefix}/task/review",
                "kind": "human_task",
                "name": "Review incident",
                "actorRole": actor_id,
                "sourceAssertionIds": [source_id_ref],
            },
            {
                "id": f"{prefix}/task/culturally-responsive-participation-support",
                "kind": "human_task",
                "name": "Provide culturally responsive participation support",
                "actorRole": actor_id,
                "sourceAssertionIds": [source_id_ref],
            },
            {
                "id": f"{prefix}/task/unresolved-questions",
                "kind": "human_task",
                "name": "Record unresolved questions",
                "actorRole": actor_id,
                "sourceAssertionIds": [source_id_ref],
            },
        ],
        "sourceAssertions": [
            {
                "id": source_id_ref,
                "authority": authority_class,
                "sourceType": "official_primary",
                "reviewStatus": "agent-proposed",
                "assertion": source_assertion,
                "sourceUri": SOURCE_REFS[source_id],
                "retrievedAt": "2026-07-03T00:00:00Z",
                "effectiveFrom": effective_from,
                "effectiveTo": None,
                "controlling": False,
            }
        ],
        "timers": [],
        "ruleInvocations": [],
        "evidenceReferences": [],
        "traces": [],
    }
    if name == "parallel-complaint":
        profile["states"].append({"id": f"{prefix}/state/parallel-pathway", "kind": "intermediate", "label": "Parallel complaint pathway", "sourceAssertionIds": [source_id_ref]})
        profile["transitions"].append(
            {
                "id": f"{prefix}/transition/parallel-pathway",
                "fromStateId": f"{prefix}/state/review",
                "toStateId": f"{prefix}/state/parallel-pathway",
                "triggerEventId": f"{prefix}/event/detected",
                "sourceAssertionIds": [source_id_ref],
            }
        )
    return profile


def write_corpus(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for scenario in SCENARIOS:
        name = scenario[0]
        path = output_dir / f"{name}.json"
        path.write_text(json.dumps(build_profile(scenario), indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    write_corpus(args.output_dir)


if __name__ == "__main__":
    main()
