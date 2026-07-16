"""Audit v1 release gates without silently treating incomplete evidence as pass."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED = {"pass", "pass_with_human_gate", "blocked", "deferred", "pending_human"}


def audit(path: Path) -> dict[str, object]:
    document = json.loads(path.read_text(encoding="utf-8"))
    diagnostics: list[str] = []
    gates = document.get("gates")
    if not isinstance(gates, list) or not gates:
        diagnostics.append("gates must be a non-empty list")
        gates = []
    seen: set[str] = set()
    for gate in gates:
        gate_id = gate.get("id") if isinstance(gate, dict) else None
        if not gate_id or gate_id in seen:
            diagnostics.append(f"missing or duplicate gate: {gate_id}")
        seen.add(gate_id)
        if gate.get("status") not in ALLOWED:
            diagnostics.append(f"unsupported gate status: {gate_id}")
        if not gate.get("evidence"):
            diagnostics.append(f"gate lacks evidence: {gate_id}")
    required = {"contracts", "hardening", "independent-validation", "human-release-authorization", "publication"}
    missing = required - seen
    diagnostics.extend(f"missing required gate: {gate_id}" for gate_id in sorted(missing))
    releasable = not diagnostics and all(gate["status"] == "pass" for gate in gates)
    return {"release": document.get("release"), "releasable": releasable, "diagnostics": diagnostics, "gateCount": len(gates)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="release/v1/gates.json")
    args = parser.parse_args()
    report = audit(Path(args.path))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not report["diagnostics"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
