import copy
import json

from tools.independent_status import GOVERNING_ISSUE, build_ledger, validate, verified_consumers


def test_committed_independent_status_is_synchronized() -> None:
    assert validate() == []


def test_generated_ledger_preserves_candidates_without_claiming_adoption() -> None:
    registry = {
        "candidates": [
            {
                "id": "candidate",
                "organisation": "External Org",
                "status": "awaiting-response",
                "outreachUrl": "https://example.org/outreach",
            }
        ]
    }
    snapshot = {"asOf": "2026-07-18", "maturityStatus": "evidence_programme_open"}
    ledger = build_ledger(registry, snapshot)
    assert ledger["governingIssue"] == GOVERNING_ISSUE
    assert ledger["qualifyingConsumers"] == []
    assert ledger["candidates"][0]["id"] == "candidate"
    assert ledger["releaseBlocking"] is False
    assert ledger["programme"] == "post_v1_ecosystem_maturity"


def test_ledger_generation_is_deterministic() -> None:
    registry = {"candidates": []}
    snapshot = {"asOf": "2026-07-18", "maturityStatus": "evidence_programme_open"}
    first = build_ledger(copy.deepcopy(registry), copy.deepcopy(snapshot))
    second = build_ledger(copy.deepcopy(registry), copy.deepcopy(snapshot))
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_generated_ledger_can_represent_post_v1_maturity_success() -> None:
    registry = {"candidates": []}
    snapshot = {
        "asOf": "2026-07-18",
        "gate": "candidate",
        "externalEvidence": "verified",
        "qualifyingConsumers": [
            {"id": "one", "maintained": True, "domainClass": "tax", "externalOrganisation": True},
            {"id": "two", "maintained": True, "domainClass": "tax", "externalOrganisation": False},
            {"id": "three", "maintained": True, "domainClass": "health", "externalOrganisation": False},
        ],
    }
    ledger = build_ledger(
        registry,
        snapshot,
        qualifying_consumers=snapshot["qualifyingConsumers"],
    )
    assert ledger["maturityStatus"] == "targets_satisfied"
    assert len(ledger["qualifyingConsumers"]) == 3


def test_empty_independent_ledger_does_not_require_a_release_gate() -> None:
    registry = {"candidates": []}
    snapshot = {"asOf": "2026-07-18", "externalEvidence": "absent"}

    ledger = build_ledger(registry, snapshot)

    assert ledger["qualifyingConsumers"] == []
    assert ledger["releaseBlocking"] is False
    assert ledger["maturityStatus"] == "evidence_programme_open"


def test_unbacked_snapshot_claim_cannot_be_counted(tmp_path) -> None:
    snapshot = {
        "asOf": "2026-07-18",
        "qualifyingConsumers": [
            {
                "id": "invented",
                "maintained": True,
                "domainClass": "tax",
                "externalOrganisation": True,
                "packetPath": "missing-packet.json",
                "evidenceRoot": "missing-evidence",
            }
        ],
    }
    qualifying, errors = verified_consumers(snapshot, root=tmp_path)
    assert qualifying == []
    assert errors and errors[0].startswith("invented:")
