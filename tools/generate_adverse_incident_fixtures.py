"""Generate synthetic adverse-incident process-profile candidates."""

from __future__ import annotations

import argparse
import hashlib
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
    actor_id = f"person:synthetic-reviewer-{name}"
    source_status = "blocked" if name == "blocked-source" else "current"
    profile: dict[str, object] = {
        "conformsTo": "pic-process-profile/0.1.0",
        "process": {"id": prefix, "version": "0.1.0-candidate", "jurisdiction": jurisdiction},
        "case": {"id": f"case:{prefix}", "synthetic": True},
        "states": [
            {"id": f"state:{name}:detected", "kind": "observed"},
            {"id": f"state:{name}:review", "kind": "proposed"},
            {"id": f"state:{name}:closed", "kind": "proposed"},
        ],
        "events": [
            {
                "id": f"event:{name}:detected",
                "kind": "observed",
                "stateId": f"state:{name}:detected",
                "occurredAt": "2026-07-01T00:00:00Z",
                "observedAt": "2026-07-01T00:00:00Z",
                "actorId": actor_id,
            }
        ],
        "transitions": [
            {
                "id": f"transition:{name}:review",
                "fromStateId": f"state:{name}:detected",
                "toStateId": f"state:{name}:review",
                "eventId": f"event:{name}:detected",
            }
        ],
        "actors": [{"id": actor_id, "kind": "person", "label": "Synthetic human reviewer"}],
        "humanTasks": [
            {
                "id": f"task:{name}:review",
                "kind": "human_review",
                "actorId": actor_id,
                "stateId": f"state:{name}:review",
            },
            {
                "id": f"task:{name}:participation-support",
                "kind": "human_decision",
                "actorId": actor_id,
                "stateId": f"state:{name}:review",
            },
            {
                "id": f"task:{name}:unresolved-questions",
                "kind": "human_review",
                "actorId": actor_id,
                "stateId": f"state:{name}:review",
            },
        ],
        "sourceAssertions": [
            {
                "id": f"assertion:{source_id}:{name}",
                "authorityClass": authority_class,
                "reviewerState": "agent-proposed",
                "sourceStatus": source_status,
                "effectiveFrom": effective_from,
                "effectiveTo": None,
                "jurisdiction": jurisdiction,
                "sourceRef": SOURCE_REFS[source_id],
                "controlling": False,
                "interpretationState": "uninterpreted",
            }
        ],
        "traceLinks": [],
    }
    trace_digest = hashlib.sha256(
        json.dumps(profile, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    profile["traceLinks"] = [
        {
            "id": f"trace-link:{name}",
            "traceConformsTo": "pic-traces/0.1.0",
            "traceRef": f"urn:sha256:{trace_digest}",
        }
    ]
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
