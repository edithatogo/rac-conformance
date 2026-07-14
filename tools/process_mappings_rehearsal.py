"""Rehearse extracting the process-mappings incubator without a remote."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

SUBTREE = Path("subrepos/process-mappings")
_MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def run_rehearsal(root: Path, report_path: Path) -> dict:
    """Copy the tracked subtree into a temporary Git repository and audit it."""

    source = root / SUBTREE
    tracked = _git(root, "ls-files", "-z", "--", str(SUBTREE)).stdout.split("\0")
    tracked = [Path(path) for path in tracked if path]
    if not tracked:
        raise ValueError("process-mappings subtree has no tracked files")
    if _git(root, "diff", "--quiet", "HEAD", "--", str(SUBTREE)).returncode != 0:
        raise ValueError("process-mappings subtree has uncommitted changes")
    if (source / ".git").exists():
        raise ValueError("nested .git directory is forbidden")

    source_commit = _git(root, "rev-parse", "HEAD").stdout.strip()
    source_tree = _git(root, "rev-parse", f"HEAD:{SUBTREE}").stdout.strip()
    file_digests = {
        str(path.relative_to(SUBTREE)): hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in tracked
    }
    file_manifest = "\n".join(f"{path}\0{digest}" for path, digest in sorted(file_digests.items()))
    file_manifest_sha = hashlib.sha256(file_manifest.encode()).hexdigest()
    license_digest = hashlib.sha256((root / "LICENSE").read_bytes()).hexdigest()

    with tempfile.TemporaryDirectory(prefix="process-mappings-rehearsal-") as temporary:
        target = Path(temporary) / "process-mappings"
        target.mkdir()
        for relative in tracked:
            destination = target / relative.relative_to(SUBTREE)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / relative, destination)
        shutil.copy2(root / "LICENSE", target / "LICENSE")

        transformed_links = _rewrite_parent_license_link(target / "LICENSE_BOUNDARY.md")
        _git(target, "init", "-q")
        _git(target, "config", "user.name", "extraction-rehearsal")
        _git(target, "config", "user.email", "rehearsal@invalid.example")
        _git(target, "add", ".")
        _git(target, "commit", "-qm", "rehearsal: import process-mappings")
        clone = Path(temporary) / "clone"
        _git(Path(temporary), "clone", "-q", str(target), str(clone))

        checks = [
            {"id": "tracked-tree", "status": "pass", "detail": f"{len(tracked)} tracked files copied"},
            {"id": "source-commit", "status": "pass", "detail": source_commit},
            {"id": "source-tree", "status": "pass", "detail": source_tree},
            {"id": "license-transfer", "status": "pass", "detail": license_digest},
            {"id": "standalone-git-commit", "status": "pass", "detail": "local commit created"},
            {"id": "independent-clone", "status": "pass", "detail": "local clone completed"},
            {"id": "link-audit", "status": "pass", "detail": "all local Markdown links resolve"},
            {"id": "provenance-files", "status": "pass", "detail": "source manifest and consumption manifest present"},
            {"id": "remote-creation", "status": "deferred", "detail": "explicit human cutover gate required"},
            {"id": "rollback", "status": "defined", "detail": "retain parent subtree until hosted clone and checks pass"},
        ]
        _assert_links(clone)
        _assert_provenance(clone)

    report = {
        "procedure": "local-process-mappings-extraction-rehearsal",
        "sourceCommit": source_commit,
        "sourceTree": source_tree,
        "trackedFileCount": len(tracked),
        "fileManifestSha256": file_manifest_sha,
        "parentLicenseSha256": license_digest,
        "transformedLinks": transformed_links,
        "checks": checks,
        "remoteCreated": False,
        "rollback": {
            "beforeCutover": "delete temporary extraction and keep parent subtree authoritative",
            "afterCutover": "restore parent reference only after canonical clone verification",
        },
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def _git(cwd: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments], cwd=cwd, check=True, capture_output=True, text=True
    )


def _rewrite_parent_license_link(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    old = "../../LICENSE"
    if old not in text:
        return []
    path.write_text(text.replace(old, "LICENSE"), encoding="utf-8")
    return [f"LICENSE_BOUNDARY.md: {old} -> LICENSE"]


def _assert_links(root: Path) -> None:
    for markdown in root.rglob("*.md"):
        for target in _MARKDOWN_LINK.findall(markdown.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#")):
                continue
            target_path = (markdown.parent / target.split("#", 1)[0]).resolve()
            if not target_path.exists():
                raise ValueError(f"broken extracted link: {markdown.name} -> {target}")


def _assert_provenance(root: Path) -> None:
    required = [
        root / "contracts/consumption.json",
        root / "profiles/foi/SOURCE_MANIFEST.json",
        root / "profiles/foi/PROFILE_CANDIDATES.json",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        raise ValueError(f"missing provenance files: {', '.join(missing)}")
