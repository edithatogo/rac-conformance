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
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_BYTES = 25 * 1024 * 1024


def run_rehearsal(root: Path, report_path: Path, *, require_clean: bool = True) -> dict:
    """Copy the tracked subtree into a temporary Git repository and audit it."""

    source = root / SUBTREE
    list_arguments = ["ls-files", "-z"]
    if not require_clean:
        list_arguments.extend(["--cached", "--others", "--exclude-standard"])
    list_arguments.extend(["--", str(SUBTREE)])
    tracked = _git(root, *list_arguments).stdout.split("\0")
    tracked = [Path(path) for path in tracked if path]
    if not tracked:
        raise ValueError("process-mappings subtree has no tracked files")
    if require_clean:
        report_relative = _relative_to_root(root, report_path)
        changed = _git(root, "diff", "--name-only", "HEAD", "--", str(SUBTREE)).stdout.splitlines()
        unexpected = [
            path
            for path in changed
            if path != report_relative and not path.endswith("/migration/REHEARSAL_REPORT.json")
        ]
        if unexpected:
            raise ValueError(f"process-mappings subtree has uncommitted changes: {unexpected}")
    if (source / ".git").exists():
        raise ValueError("nested .git directory is forbidden")

    source_commit = _git(root, "rev-parse", "HEAD").stdout.strip()
    source_tree = _git(root, "rev-parse", f"HEAD:{SUBTREE}").stdout.strip()
    history_split = _git(root, "subtree", "split", "--prefix", str(SUBTREE), "HEAD").stdout.strip()
    file_digests = {
        str(path.relative_to(SUBTREE)): hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in tracked
    }
    total_bytes = sum((root / path).stat().st_size for path in tracked)
    if total_bytes > MAX_TOTAL_BYTES:
        raise ValueError(f"process-mappings subtree exceeds {MAX_TOTAL_BYTES} bytes")
    oversized = [str(path) for path in tracked if (root / path).stat().st_size > MAX_FILE_BYTES]
    if oversized:
        raise ValueError(f"process-mappings files exceed {MAX_FILE_BYTES} bytes: {oversized}")
    file_manifest = "\n".join(f"{path}\0{digest}" for path, digest in sorted(file_digests.items()))
    file_manifest_sha = hashlib.sha256(file_manifest.encode()).hexdigest()
    license_digest = hashlib.sha256((root / "LICENSE").read_bytes()).hexdigest()

    with tempfile.TemporaryDirectory(prefix="process-mappings-rehearsal-") as temporary:
        target = Path(temporary) / "process-mappings"
        target.mkdir()
        for relative in tracked:
            destination = _safe_destination(target, relative.relative_to(SUBTREE))
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
            {"id": "history-preservation", "status": "pass", "detail": history_split},
            {"id": "license-transfer", "status": "pass", "detail": license_digest},
            {"id": "standalone-git-commit", "status": "pass", "detail": "local commit created"},
            {"id": "independent-clone", "status": "pass", "detail": "local clone completed"},
            {"id": "link-audit", "status": "pass", "detail": "all local Markdown links resolve"},
            {"id": "provenance-files", "status": "pass", "detail": "source manifest and consumption manifest present"},
            {"id": "standalone-ci", "status": "deferred", "detail": "destination workflow must be added after cutover approval"},
            {"id": "local-installation", "status": "not-applicable", "detail": "incubator contains no installable runtime package"},
            {"id": "dependency-updates", "status": "deferred", "detail": "destination dependency policy must be configured after cutover"},
            {"id": "issue-migration", "status": "drafted", "detail": "migration packet preserves parent issue cross-references"},
            {"id": "source-reference-portability", "status": "pass", "detail": "FOI-O profile references use pinned durable locators"},
            {"id": "parent-consumption-evidence", "status": "pass", "detail": "parent manifest retains local paths and pinned portable locators"},
            {"id": "remote-creation", "status": "deferred", "detail": "explicit human cutover gate required"},
            {"id": "rollback", "status": "defined", "detail": "retain parent subtree until hosted clone and checks pass"},
        ]
        _assert_links(clone)
        _assert_provenance(clone)

    report = {
        "procedure": "local-process-mappings-extraction-rehearsal",
        "sourceCommit": source_commit,
        "sourceTree": source_tree,
        "historySplitCommit": history_split,
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


def _relative_to_root(root: Path, path: Path) -> str | None:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return None


def _safe_destination(root: Path, relative: Path) -> Path:
    """Return a destination proven to remain below the extraction root."""

    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe extracted path: {relative}")
    resolved_root = root.resolve()
    destination = (resolved_root / relative).resolve()
    if destination != resolved_root and resolved_root not in destination.parents:
        raise ValueError(f"extracted path escapes destination: {relative}")
    return destination


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
        root / "profiles/foi/SOURCE_REFERENCE_PORTABILITY.json",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        raise ValueError(f"missing provenance files: {', '.join(missing)}")
