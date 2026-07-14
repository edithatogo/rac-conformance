#!/usr/bin/env python3
"""Validate the paper programme's version and citation/mirror register."""
from __future__ import annotations
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "papers/zenodo/foi-programme-mirror-manifest.json"


def validate_commit_pin(item: dict[str, object]) -> None:
    """Require immutable commit evidence for integration release artifacts."""
    if item["kind"] != "software_and_integration":
        return
    commit = item.get("commit")
    assert isinstance(commit, str), item["id"]
    assert len(commit) == 40, item["id"]
    assert all(character in "0123456789abcdef" for character in commit), item["id"]


def repository_root(artifact_id: str) -> Path:
    """Resolve a sibling checkout without assuming a developer's filesystem."""
    if artifact_id == "rac-conformance":
        return ROOT
    programme_root = Path(
        os.environ.get("FOI_PROGRAMME_REPO_ROOT", str(ROOT.parent)),
    )
    return programme_root / artifact_id

def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    expected = {
        "foi-o",
        "fyi-cli",
        "fyi-archive",
        "nlp-policy-nz",
        "legislation",
        "rac-conformance",
        "foi-process",
        "alaveteli",
        "foi-programme-quality-evidence",
        "foio-pic-release-evidence",
    }
    assert {item["id"] for item in data["artifacts"]} == expected
    for item in data["artifacts"]:
        validate_commit_pin(item)
        if item["zenodo_status"] == "verified_published_version":
            assert item["zenodo_doi"], item["id"]
        if item["zenodo_status"] == "published_record_version_mismatch":
            assert item["zenodo_doi"], item["id"]
            assert item["zenodo_record_version"] != item["version"], item["id"]
        huggingface = item.get("huggingface_target")
        if isinstance(huggingface, dict):
            assert len(huggingface["revision"]) == 40, item["id"]
            assert len(huggingface["artifact_sha256"]) == 64, item["id"]
            if huggingface["status"] == "pinned_with_provenance_exception":
                assert huggingface["exceptions"], item["id"]
        if item["kind"] == "release_evidence":
            assert (ROOT / item["artifact_path"]).is_file(), item["id"]
        elif item["kind"] != "upstream_workflow_intelligence":
            citation_path = repository_root(item["id"]) / item["citation_file"]
            assert citation_path.is_file(), (
                f"{item['id']}: missing {citation_path}; check "
                "FOI_PROGRAMME_REPO_ROOT"
            )
            assert item["version"] and item["tag"], item["id"]
    print(f"validated {len(data['artifacts'])} programme artefacts")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
