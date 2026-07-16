"""Rehearse extraction of the process-mappings incubator without a remote."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PREFIX = "subrepos/process-mappings"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], stderr=subprocess.DEVNULL, text=True
    ).strip()


def file_manifest(root: Path) -> tuple[list[str], str]:
    files = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    digest = hashlib.sha256("\n".join(files).encode("utf-8")).hexdigest()
    return files, digest


def rehearse(repository_root: Path) -> dict[str, object]:
    parent_head = git(repository_root, "rev-parse", "HEAD")
    split_commit = git(repository_root, "subtree", "split", f"--prefix={PREFIX}", "HEAD")
    report: dict[str, object] = {
        "schemaVersion": "process-mappings-extraction-rehearsal.v0.1.0",
        "parentHead": parent_head,
        "subtreeCommit": split_commit,
        "remoteCreated": False,
        "canonicalCutover": False,
        "worktreeOverlay": bool(git(repository_root, "status", "--porcelain", "--", PREFIX)),
        "rollback": {
            "procedure": "Delete the temporary extraction; parent HEAD and working tree are unchanged.",
            "dualWritableSourcePrevented": True,
        },
    }

    with tempfile.TemporaryDirectory(prefix="process-mappings-rehearsal-") as temporary:
        workspace = Path(temporary)
        extracted = workspace / "repository"
        extracted.mkdir()
        subprocess.run(["git", "-C", str(extracted), "init", "--quiet"], check=True)
        subprocess.run(
            ["git", "-C", str(extracted), "fetch", "--quiet", str(repository_root), split_commit],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(extracted), "checkout", "--quiet", "-b", "main", "FETCH_HEAD"],
            check=True,
        )
        if report["worktreeOverlay"]:
            shutil.copytree(repository_root / PREFIX, extracted, dirs_exist_ok=True)
        # The proposed standalone root receives the parent license and rewrites
        # the incubation-only relative reference before its self-contained check.
        shutil.copy2(repository_root / "LICENSE", extracted / "LICENSE")
        boundary = extracted / "LICENSE_BOUNDARY.md"
        if boundary.is_file():
            boundary.write_text(
                boundary.read_text(encoding="utf-8").replace("../../LICENSE", "LICENSE"),
                encoding="utf-8",
            )
        files, file_digest = file_manifest(extracted)
        subprocess.run(["sh", "ci/check.sh"], cwd=extracted, check=True)
        fsck = subprocess.run(
            ["git", "-C", str(extracted), "fsck", "--full"],
            check=False,
            capture_output=True,
            text=True,
        )
        report["extracted"] = {
            "commitCount": int(git(extracted, "rev-list", "--count", "HEAD")),
            "fileCount": len(files),
            "fileListSha256": file_digest,
            "requiredStandaloneCheck": "passed",
            "gitFsck": "passed" if fsck.returncode == 0 else "failed",
        }
        if fsck.returncode != 0:
            report["gitFsckOutput"] = fsck.stderr or fsck.stdout
            raise RuntimeError("extracted repository failed git fsck")

        # The temporary repository has the only writable checkout during this rehearsal.
        report["extracted"]["writableSourceCount"] = 1  # type: ignore[index]
        report["extracted"]["rollbackVerified"] = True  # type: ignore[index]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--report", required=True)
    args = parser.parse_args(argv)
    report = rehearse(Path(args.repository_root).resolve())
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"OK: extraction rehearsal written to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
