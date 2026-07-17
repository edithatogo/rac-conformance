from __future__ import annotations

import json
from pathlib import Path

from tools.validate_health_technology_matrix import validate


ROOT = Path(__file__).parents[2] / "subrepos/process-mappings/profiles/health-technology"


def test_health_technology_matrix_is_valid() -> None:
    assert validate(ROOT) == []


def test_matrix_rejects_fda_as_payer(tmp_path: Path) -> None:
    matrix = json.loads((ROOT / "authority-matrix.json").read_text(encoding="utf-8"))
    for jurisdiction in matrix["jurisdictions"]:
        for authority in jurisdiction["authorities"]:
            if authority["id"] == "fda":
                authority["roles"].append("payer_coverage")
    root = tmp_path / "health-technology"
    (root / "sources").mkdir(parents=True)
    (root / "authority-matrix.json").write_text(json.dumps(matrix), encoding="utf-8")
    (root / "sources/manifest.json").write_text((ROOT / "sources/manifest.json").read_text(encoding="utf-8"), encoding="utf-8")
    assert any("FDA" in error for error in validate(root))


def test_matrix_rejects_mbs_as_medicine_regulator(tmp_path: Path) -> None:
    matrix = json.loads((ROOT / "authority-matrix.json").read_text(encoding="utf-8"))
    for jurisdiction in matrix["jurisdictions"]:
        for authority in jurisdiction["authorities"]:
            if authority["id"] == "mbs":
                authority["roles"].append("market_authorisation")
    root = tmp_path / "health-technology"
    (root / "sources").mkdir(parents=True)
    (root / "authority-matrix.json").write_text(json.dumps(matrix), encoding="utf-8")
    (root / "sources/manifest.json").write_text((ROOT / "sources/manifest.json").read_text(encoding="utf-8"), encoding="utf-8")
    assert any("MBS" in error for error in validate(root))


def test_comparison_packet_records_selection_without_promotion() -> None:
    packet = json.loads((ROOT / "comparison-candidates.json").read_text(encoding="utf-8"))
    assert packet["selection"] == "pembrolizumab-adjuvant-stage-iii-melanoma"
    assert packet["selectionStatus"] == "human-selected-source-verification-authorized"
    selected = next(candidate for candidate in packet["candidates"] if candidate["id"] == packet["selection"])
    assert selected["status"] == "selected-source-verification-required"
    assert "not certified" in packet["promotionBoundary"]
    assert all(candidate["status"] == "not-selected" for candidate in packet["candidates"] if candidate is not selected)


def test_source_manifest_rejects_malformed_source_entry(tmp_path: Path) -> None:
    matrix = json.loads((ROOT / "authority-matrix.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "sources/manifest.json").read_text(encoding="utf-8"))
    manifest["sources"].append({"verificationStatus": "observed"})
    root = tmp_path / "health-technology"
    (root / "sources").mkdir(parents=True)
    (root / "authority-matrix.json").write_text(json.dumps(matrix), encoding="utf-8")
    (root / "sources/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    assert any("missing 'id'" in error for error in validate(root))


def test_selected_source_spine_has_direct_capture_and_explicit_date_gaps() -> None:
    spine = json.loads(
        (ROOT / "candidates/SOURCE_SPINE.json").read_text(encoding="utf-8")
    )
    sources = {source["id"]: source for source in spine["sources"]}
    for source_id in (
        "nz-medsafe-evaluation",
        "nz-pharmac-funding-journey",
        "nz-pharmac-melanoma-2025",
        "uk-mhra-market-authorisation",
        "uk-nice-process-manual",
        "uk-nice-ta766",
    ):
        source = sources[source_id]
        assert source["sourceStatus"].startswith("official-")
        assert source["retrievalDigest"].startswith("sha256:")
        assert source["url"].startswith("https://")
    assert sources["nz-medsafe-evaluation"]["effectiveDateStatus"] == "missing-on-source-page"
    assert sources["uk-mhra-market-authorisation"]["effectiveDateStatus"] == "missing-on-source-page"
    assert "Human review" in spine["promotionBoundary"]
