from datetime import date
import json
from pathlib import Path

from tools.v1_release_audit import audit


ROOT = Path(__file__).resolve().parents[2]


def test_current_release_audit_preserves_blockers():
    manifest = json.loads((ROOT / "conductor/v1-release-gates.json").read_text())
    report = audit(manifest, as_of=date(2026, 7, 15))

    assert report["manifestValid"] is True
    assert report["releaseDecision"] == "blocked"
    assert {item["id"] for item in report["blockers"]} == {
        "foio-release-evidence-bundle",
        "external-independent-adoption",
        "papers-refresh",
        "papers-programme-submission",
        "rac-zenodo-deposit",
        "foi-governance-manual-verification",
    }
    assert report["networkChecks"] == "not-performed"


def test_audit_is_ready_only_when_every_gate_passes():
    manifest = {
        "manifest_version": "1",
        "release": "v1.0.0-rc.1",
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


def test_audit_reports_malformed_gate_entries_without_crashing():
    manifest = {
        "manifest_version": "1",
        "release": "v1.0.0-rc.1",
        "gates": ["malformed"],
    }

    report = audit(manifest, as_of=date(2026, 7, 15))

    assert report["manifestValid"] is False
    assert report["releaseDecision"] == "blocked"
