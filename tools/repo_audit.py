"""Deterministic repository and manuscript integrity checks."""

from __future__ import annotations

import re
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_REPOSITORY = "github.com/edithatogo/rulesandprocesses"
CANONICAL_REPOSITORY = "github.com/edithatogo/rac-conformance"
LEGACY_ID_PATHS = {
    Path("contracts/pic-crosswalk/0.1.0/schema.json"),
    Path("contracts/pic-fixtures/0.1.0/schema.json"),
    Path("contracts/pic-parameters/0.1.0/schema.json"),
    Path("contracts/pic-parameters/0.2.0/schema.json"),
    Path("contracts/pic-semantics/0.1.0/schema.json"),
    Path("independent/kit/bundle/pic-semantics-0.1.0/schema.json"),
    Path("contracts/pic-traces/0.1.0/schema.json"),
    Path("contracts/pic-traces/0.2.0/schema.json"),
    Path("conductor/archive/contracts_20260704/plan.md"),
}
INTENTIONAL_LEGACY_REFERENCE_PATHS = LEGACY_ID_PATHS | {
    Path("tools/repo_audit.py"),
    Path("docs/REPOSITORY_IDENTITY.md"),
}
MANUSCRIPTS = (
    ROOT / "papers/coupling/paper.md",
    ROOT / "studies/snap-divergence/paper/paper.md",
    ROOT / "studies/nz-reconciliation/paper/paper.md",
)
REQUIRED_SECTIONS = (
    "## Abstract",
    "## Data and code availability",
    "## Limitations",
)
FORBIDDEN_PATTERNS = {
    r"100% differential testing parity": "overstates the evaluated corpus",
    r"65 human-curated": "misstates mixed fixture provenance",
    r"no divergences represent programming errors": "overstates unresolved adjudication",
}


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^]]+\]\(([^)]+)\)", text)


def audit_manuscript(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [f"{path}: missing {section}" for section in REQUIRED_SECTIONS if section not in text]
    for pattern, reason in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{path}: {reason}: /{pattern}/")
    for target in markdown_links(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        candidate = (path.parent / target.split("#", 1)[0]).resolve()
        if not candidate.exists():
            errors.append(f"{path}: broken local link {target}")
    return errors


def audit_repository(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    required = (
        root / ".github/PULL_REQUEST_TEMPLATE.md",
        root / ".github/CODEOWNERS",
        root / ".github/dependabot.yml",
        root / "SECURITY.md",
    )
    errors.extend(f"missing required governance file: {path}" for path in required if not path.exists())
    for path in MANUSCRIPTS:
        errors.extend(audit_manuscript(path))
    excluded = {".git", ".venv", ".external-repos", "__pycache__", ".pytest_cache", "conversation", "source_material"}
    for root_dir, directories, filenames in os.walk(root):
        directories[:] = [directory for directory in directories if directory not in excluded]
        for filename in filenames:
            path = Path(root_dir) / filename
            relative = path.relative_to(root)
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if LEGACY_REPOSITORY in text and relative not in INTENTIONAL_LEGACY_REFERENCE_PATHS:
                errors.append(f"{relative}: unexpected legacy repository URL")
    citation_path = root / "CITATION.cff"
    if citation_path.exists():
        citation = citation_path.read_text(encoding="utf-8")
        if CANONICAL_REPOSITORY not in citation:
            errors.append("CITATION.cff: canonical repository URL is missing")
    else:
        errors.append("CITATION.cff: file is missing")
    return errors


def main() -> int:
    errors = audit_repository()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("repository audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
