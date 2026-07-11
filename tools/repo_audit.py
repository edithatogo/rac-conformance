"""Deterministic repository and manuscript integrity checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPTS = (
    ROOT / "papers/coupling/paper.md",
    ROOT / "studies/snap-divergence/paper/paper.md",
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
