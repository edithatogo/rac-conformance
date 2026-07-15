from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_gate_confirmations_fail_closed_until_attributable_evidence_exists() -> None:
    packet = json.loads((ROOT / "conductor/PROGRAMME_GATE_CONFIRMATIONS.json").read_text())
    assert {item["issue"] for item in packet["confirmations"]} == {"#23", "#27", "#30", "#31", "#33"}
    for item in packet["confirmations"]:
        assert item["status"].startswith("pending_")
        assert item["evidenceUrl"] is None
        assert item["confirmedBy"] is None
        assert item["confirmedAt"] is None
