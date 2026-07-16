from __future__ import annotations

import json
from pathlib import Path

from tools.validate_health_technology_matrix import validate


ROOT = Path(__file__).parents[2] / "subrepos/process-mappings/profiles/health-technology"


def test_health_technology_matrix_is_valid() -> None:
    assert validate(ROOT) == []


def test_matrix_rejects_fda_as_payer(tmp_path: Path) -> None:
    matrix = json.loads((ROOT / "authority-matrix.json").read_text())
    for jurisdiction in matrix["jurisdictions"]:
        for authority in jurisdiction["authorities"]:
            if authority["id"] == "fda":
                authority["roles"].append("payer_coverage")
    root = tmp_path / "health-technology"
    (root / "sources").mkdir(parents=True)
    (root / "authority-matrix.json").write_text(json.dumps(matrix))
    (root / "sources/manifest.json").write_text((ROOT / "sources/manifest.json").read_text())
    assert any("FDA" in error for error in validate(root))


def test_matrix_rejects_mbs_as_medicine_regulator(tmp_path: Path) -> None:
    matrix = json.loads((ROOT / "authority-matrix.json").read_text())
    for jurisdiction in matrix["jurisdictions"]:
        for authority in jurisdiction["authorities"]:
            if authority["id"] == "mbs":
                authority["roles"].append("market_authorisation")
    root = tmp_path / "health-technology"
    (root / "sources").mkdir(parents=True)
    (root / "authority-matrix.json").write_text(json.dumps(matrix))
    (root / "sources/manifest.json").write_text((ROOT / "sources/manifest.json").read_text())
    assert any("MBS" in error for error in validate(root))


def test_comparison_packet_does_not_promote_unselected_candidates() -> None:
    packet = json.loads((ROOT / "comparison-candidates.json").read_text())
    assert packet["selection"] == "none"
    assert all(candidate["status"] == "deferred" for candidate in packet["candidates"])
