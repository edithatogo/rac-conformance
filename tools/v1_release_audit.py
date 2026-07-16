"""Create a deterministic v1 release-readiness report from the gate manifest."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from tools.release_gates import load_manifest, validate_manifest


def audit(manifest: dict, *, as_of: date) -> dict:
    validation = validate_manifest(manifest, as_of=as_of)
    gates = sorted(
        (gate for gate in manifest.get("gates", []) if isinstance(gate, dict)),
        key=lambda gate: str(gate.get("id", "")),
    )
    blockers = [
        {
            "id": gate.get("id"),
            "status": gate.get("status"),
            "reasonCode": gate.get("reason_code"),
            "nextAction": gate.get("next_action"),
            "dependencies": gate.get("dependencies", []),
        }
        for gate in gates
        if gate.get("status") in {"blocked", "fail", "exception"}
    ]
    return {
        "schemaVersion": "rac-v1-release-audit.v1",
        "asOf": as_of.isoformat(),
        "release": manifest.get("release"),
        "manifestValid": validation.ok,
        "releaseDecision": "ready" if validation.ok and not blockers else "blocked",
        "networkChecks": "not-performed",
        "statuses": sorted(validation.statuses),
        "validationErrors": list(validation.errors),
        "gateCount": len(gates),
        "blockers": blockers,
        "gates": [
            {
                "id": gate.get("id"),
                "owner": gate.get("owner"),
                "category": gate.get("category"),
                "status": gate.get("status"),
                "observedAt": gate.get("observed_at"),
            }
            for gate in gates
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit v1 release readiness")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--as-of", required=True, type=date.fromisoformat)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = audit(load_manifest(args.manifest), as_of=args.as_of)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["releaseDecision"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
