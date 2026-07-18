"""Generate and validate synchronized independent-validation status."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path

from tools.independent_evidence import classify

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "external/independent-validation/CANDIDATE_REGISTRY.json"
SNAPSHOT = ROOT / "external/independent-validation/STATUS_SNAPSHOT.json"
LEDGER = ROOT / "independent/STATUS_LEDGER.json"
RELEASE_GATES = ROOT / "conductor/v1-release-gates.json"
GOVERNING_ISSUE = "https://github.com/edithatogo/rac-conformance/issues/45"


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def _safe_path(root: Path, value: str) -> Path:
    resolved_root = root.resolve()
    path = (resolved_root / value).resolve()
    if path == resolved_root or resolved_root not in path.parents:
        raise ValueError(f"status evidence path escapes repository: {value}")
    return path


def verified_consumers(snapshot: dict, *, root: Path = ROOT) -> tuple[list[dict], list[str]]:
    verified = []
    errors = []
    for claim in snapshot.get("qualifyingConsumers", []):
        claim_id = claim.get("id", "<missing-id>")
        try:
            packet_path = _safe_path(root, claim["packetPath"])
            evidence_root = _safe_path(root, claim["evidenceRoot"])
            packet = _load(packet_path)
            report = classify(
                packet,
                evidence_root=evidence_root,
                today=date.fromisoformat(snapshot["asOf"]),
            )
        except (KeyError, OSError, TypeError, ValueError) as exc:
            errors.append(f"{claim_id}: independent evidence cannot be loaded: {exc}")
            continue
        if not report["qualifiesForV1"]:
            errors.append(f"{claim_id}: independent evidence is not qualifying")
            continue
        verified.append(
            {
                "id": claim["id"],
                "maintained": claim["maintained"],
                "domainClass": claim["domainClass"],
                "externalOrganisation": claim["externalOrganisation"],
                "packetPath": claim["packetPath"],
                "evidenceRoot": claim["evidenceRoot"],
            }
        )
    return verified, errors


def build_ledger(
    registry: dict,
    snapshot: dict,
    *,
    qualifying_consumers: list[dict] | None = None,
) -> dict:
    candidates = [
        {
            "id": candidate["id"],
            "organisation": candidate["organisation"],
            "status": candidate["status"],
            **({"outreachUrl": candidate["outreachUrl"]} if candidate.get("outreachUrl") else {}),
        }
        for candidate in registry["candidates"]
    ]
    requirements = {
        "maintainedConsumers": 3,
        "domainClasses": 2,
        "externalImplementation": 1,
    }
    qualifying = qualifying_consumers or []
    maintained = [consumer for consumer in qualifying if consumer.get("maintained") is True]
    domains = {consumer.get("domainClass") for consumer in maintained if consumer.get("domainClass")}
    external = [consumer for consumer in maintained if consumer.get("externalOrganisation") is True]
    satisfied = (
        len(maintained) >= requirements["maintainedConsumers"]
        and len(domains) >= requirements["domainClasses"]
        and len(external) >= requirements["externalImplementation"]
    )
    return {
        "schemaVersion": "rac-independent-adoption-ledger.v0.2.0",
        "updatedAt": snapshot["asOf"],
        "governingIssue": GOVERNING_ISSUE,
        "evidenceContract": "rac-independent-submission.v2",
        "requiredForV1": requirements,
        "qualifyingConsumers": qualifying,
        "candidates": candidates,
        "gate": "satisfied" if satisfied else "blocked_pending_external_evidence",
        "reason": (
            "Published v2 evidence satisfies the independent-adoption thresholds."
            if satisfied
            else "No sufficient set of independently controlled v2 evidence bundles has been verified and acknowledged."
        ),
    }


def validate() -> list[str]:
    registry = _load(REGISTRY)
    snapshot = _load(SNAPSHOT)
    ledger = _load(LEDGER)
    release = _load(RELEASE_GATES)
    qualifying, errors = verified_consumers(snapshot)
    expected = build_ledger(registry, snapshot, qualifying_consumers=qualifying)
    if ledger != expected:
        errors.append("independent/STATUS_LEDGER.json is not synchronized")
    adoption = next(
        (gate for gate in release.get("gates", []) if gate.get("id") == "external-independent-adoption"),
        None,
    )
    if adoption is None:
        errors.append("release manifest lacks external-independent-adoption gate")
    else:
        if adoption.get("source") != GOVERNING_ISSUE:
            errors.append("independent-adoption gate does not point to issue 45")
        expected_status = "pass" if ledger.get("gate") == "satisfied" else "blocked"
        if adoption.get("status") != expected_status:
            errors.append("independent-adoption gate status does not match the evidence ledger")
        if adoption.get("observed_at") != snapshot.get("asOf"):
            errors.append("independent-adoption gate observation date is not synchronized")
    if snapshot.get("externalEvidence") == "absent" and ledger.get("qualifyingConsumers"):
        errors.append("ledger claims qualifying consumers without external evidence")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.write:
        snapshot = _load(SNAPSHOT)
        qualifying, errors = verified_consumers(snapshot)
        if errors:
            print("\n".join(errors))
            return 1
        LEDGER.write_text(
            json.dumps(
                build_ledger(
                    _load(REGISTRY),
                    snapshot,
                    qualifying_consumers=qualifying,
                ),
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    errors = validate()
    if errors:
        print("\n".join(errors))
        return 1
    print("independent-validation status is synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
