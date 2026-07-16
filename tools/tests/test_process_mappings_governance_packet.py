"""Tests for the human-gated process-mappings migration packet."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
SUBTREE = ROOT / "subrepos/process-mappings"
PACKET = ROOT / "conductor/tracks/process_mappings_repository_20260714/GITHUB_MIGRATION_PACKET.md"


def test_prepared_governance_files_and_packet_are_present() -> None:
    for relative in (
        ".github/CODEOWNERS",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/profile.yml",
        ".github/ISSUE_TEMPLATE/bug.yml",
        "SECURITY.md",
        "ci/check.sh",
    ):
        assert (SUBTREE / relative).is_file()
    content = PACKET.read_text(encoding="utf-8")
    assert "human approval required" in content
    assert "does not create a remote" in content
    assert "Project 19" in content
    assert "single writable canonical source" in content
