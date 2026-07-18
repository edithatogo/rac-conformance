import json
from pathlib import Path

import yaml


ROOT = Path(__file__).parents[2]


def test_sbom_is_spdx_and_names_lockfile_digest() -> None:
    sbom = json.loads((ROOT / "security/SBOM.spdx.json").read_text())
    assert sbom["spdxVersion"] == "SPDX-2.3"
    assert any(package["name"] == "contracts/tools/uv.lock" for package in sbom["packages"])


def test_provenance_packet_preserves_unmet_evidence_boundary() -> None:
    text = (ROOT / "security/PROVENANCE.md").read_text()
    assert "remain release-blocking" in text


def test_rollback_packet_preserves_human_gate() -> None:
    text = (ROOT / "security/ROLLBACK_REHEARSAL.md").read_text()
    assert "human approval" in text


def test_release_workflow_requires_ready_audit_before_attestation() -> None:
    workflow = yaml.safe_load(
        (ROOT / ".github/workflows/v1-release-qualification.yml").read_text()
    )
    steps = workflow["jobs"]["qualify-candidate"]["steps"]
    audit_index = next(
        (
            index
            for index, step in enumerate(steps)
            if "tools.v1_release_audit" in (step.get("run") or "")
        ),
        None,
    )
    assert audit_index is not None, "release audit step not found"
    attestation_index = next(
        (
            index
            for index, step in enumerate(steps)
            if str(step.get("uses") or "").startswith(
                "actions/attest-build-provenance@"
            )
        ),
        None,
    )
    assert attestation_index is not None, "build provenance attestation step not found"
    assert audit_index < attestation_index
    assert "V1_RELEASE_GATE_AUDIT.json" in (steps[audit_index].get("run") or "")
