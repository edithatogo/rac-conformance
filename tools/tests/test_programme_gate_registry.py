from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_programme_gate_registry_is_fail_closed_and_evidence_linked() -> None:
    registry = json.loads((ROOT / "conductor/PROGRAMME_GATE_REGISTRY.json").read_text())
    assert registry["schemaVersion"] == "rac-programme-gates.v1"
    assert (ROOT / registry["actionPacket"]).exists()
    assert (ROOT / registry["confirmationLedger"]).exists()
    assert {gate["issue"] for gate in registry["gates"]} == {"#23", "#24", "#30", "#31", "#33"}
    for gate in registry["gates"]:
        assert gate["status"] != "pass"
        assert gate["localEvidence"]
        assert all((ROOT / path).exists() for path in gate["localEvidence"])
        assert gate["nextAction"]
        assert gate["preparationStatus"]
