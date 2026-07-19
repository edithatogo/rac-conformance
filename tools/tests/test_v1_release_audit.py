from datetime import date
import json
from pathlib import Path

from tools.v1_release_audit import audit


ROOT = Path(__file__).resolve().parents[2]


def test_current_release_audit_preserves_blockers():
    manifest = json.loads((ROOT / "conductor/v1-release-gates.json").read_text())
    report = audit(manifest, as_of=date(2026, 7, 17))

    assert report["manifestValid"] is True
    assert report["releaseDecision"] == "blocked"
    assert {item["id"] for item in report["blockers"]} == {
        "foio-release-evidence-bundle",
        "papers-refresh",
        "papers-programme-submission",
        "rac-zenodo-deposit",
    }
    assert report["networkChecks"] == "not-performed"


def test_upstream_silence_is_not_a_v1_release_gate():
    manifest = json.loads((ROOT / "conductor/v1-release-gates.json").read_text())

    assert "external-independent-adoption" not in {
        gate["id"] for gate in manifest["gates"]
    }


def test_audit_is_ready_only_when_every_declared_gate_passes():
    manifest = {
        "manifest_version": "1",
        "release": "v1.0.0-rc.1",
        "required_gate_ids": ["local"],
        "gates": [
            {
                "id": "local",
                "owner": "maintainers",
                "category": "repository",
                "status": "pass",
                "observed_at": "2026-07-15",
                "evidence": [{"digest": "sha256:abc", "observed_at": "2026-07-15"}],
            }
        ],
    }
    assert audit(manifest, as_of=date(2026, 7, 15))["releaseDecision"] == "ready"


def test_audit_fails_closed_when_required_gate_inventory_is_absent():
    manifest = {
        "manifest_version": "1",
        "release": "v1.0.0-rc.1",
        "gates": [],
    }

    report = audit(manifest, as_of=date(2026, 7, 15))

    assert report["manifestValid"] is False
    assert report["releaseDecision"] == "blocked"
    assert "required_gate_ids must be a non-empty list" in report["validationErrors"]


def test_audit_fails_closed_when_a_required_gate_is_missing():
    manifest = {
        "manifest_version": "1",
        "release": "v1.0.0-rc.1",
        "required_gate_ids": ["local", "authorization"],
        "gates": [
            {
                "id": "local",
                "owner": "maintainers",
                "category": "repository",
                "status": "pass",
                "observed_at": "2026-07-15",
                "evidence": [{"digest": "sha256:abc", "observed_at": "2026-07-15"}],
            }
        ],
    }

    report = audit(manifest, as_of=date(2026, 7, 15))

    assert report["releaseDecision"] == "blocked"
    assert report["missingRequiredGates"] == ["authorization"]


def test_audit_reports_malformed_gate_entries_without_crashing():
    manifest = {
        "manifest_version": "1",
        "release": "v1.0.0-rc.1",
        "required_gate_ids": ["local"],
        "gates": ["malformed"],
    }

    report = audit(manifest, as_of=date(2026, 7, 15))

    assert report["manifestValid"] is False
    assert report["releaseDecision"] == "blocked"
