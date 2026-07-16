"""Verify the extracted process-mappings repository without parent dependencies."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


IMMUTABLE = re.compile(r"^(?:v[0-9]+\.[0-9]+\.[0-9]+|[0-9a-f]{40})$")
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED = (
    "README.md",
    "LICENSE_BOUNDARY.md",
    "REPOSITORY_BOUNDARY.md",
    "STATUS.md",
    "schemas/contract-consumption.json",
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    manifest_path = root / "schemas/contract-consumption.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"contract manifest is not JSON: {exc}")
        else:
            if manifest.get("schemaVersion") != "process-mappings-contract-consumption.v0.1.0":
                errors.append("contract manifest has an unsupported schemaVersion")
            repository = manifest.get("repository", {})
            if not IMMUTABLE.fullmatch(repository.get("revision", "")):
                errors.append("contract manifest repository revision is not immutable")
            for source in manifest.get("inputs", []):
                if not IMMUTABLE.fullmatch(source.get("revision", "")):
                    errors.append(f"source revision is not immutable: {source.get('id')}")
                if not re.fullmatch(r"[0-9a-f]{64}", source.get("sha256", "")):
                    errors.append(f"source digest is invalid: {source.get('id')}")

    contracts_root = root / "contracts"
    if contracts_root.exists():
        unexpected = [path for path in contracts_root.rglob("*") if path.is_file() and path.name != "consumption.json"]
        if unexpected:
            errors.append("normative PIC contracts were copied into the extracted repository")
    nested_git = [path for path in root.rglob(".git") if path != root / ".git"]
    if nested_git:
        errors.append("nested Git repository detected")

    for markdown in root.rglob("*.md"):
        for target in LINK.findall(markdown.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = (markdown.parent / target.split("#", 1)[0]).resolve()
            if not path.is_file() or root not in path.parents:
                errors.append(f"broken relative link: {markdown.relative_to(root)} -> {target}")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: standalone process-mappings checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
