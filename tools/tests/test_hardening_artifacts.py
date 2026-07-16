import json
from pathlib import Path


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
