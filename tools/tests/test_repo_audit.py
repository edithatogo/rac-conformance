from pathlib import Path

import yaml

from tools.repo_audit import audit_manuscript, markdown_links


def test_markdown_links_extract_targets() -> None:
    assert markdown_links("See [local](../x.md) and [web](https://example.com).") == [
        "../x.md",
        "https://example.com",
    ]


def test_audit_rejects_unsupported_claim_and_broken_link(tmp_path: Path) -> None:
    manuscript = tmp_path / "paper.md"
    manuscript.write_text(
        "## Abstract\n100% differential testing parity\n"
        "## Data and code availability\n[missing](missing.md)\n## Limitations\n",
        encoding="utf-8",
    )
    errors = audit_manuscript(manuscript)
    assert any("overstates" in error for error in errors)
    assert any("broken local link" in error for error in errors)


def test_workflows_keep_triggers_at_top_level() -> None:
    workflows = Path(".github/workflows").glob("*.yml")
    for workflow in workflows:
        document = yaml.load(workflow.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        assert "on" in document, f"{workflow} has no trigger block"
        assert "pull_request" not in document.get("concurrency", {}), (
            f"{workflow} nests pull_request under concurrency"
        )
