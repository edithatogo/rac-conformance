"""Rehearse restoring source trees from current and historical Git commits."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from v1_reproducibility import _archive, _git, _sha256

ROOT = Path(__file__).resolve().parents[1]
FALLBACK = "v0.2.0"
REQUIRED_PATHS = ("LICENSE", "contracts", "conductor", "SECURITY.md")


def _extract(archive: Path, target: Path) -> list[str]:
    target.mkdir()
    subprocess.run(["tar", "-xzf", str(archive), "-C", str(target)], check=True)
    restored = target / "rac-conformance"
    return [path for path in REQUIRED_PATHS if (restored / path).exists()]


def build_report() -> dict[str, object]:
    current = _git("rev-parse", "HEAD")
    fallback = _git("rev-parse", FALLBACK)
    with tempfile.TemporaryDirectory(prefix="rac-v1-rollback-") as temporary:
        directory = Path(temporary)
        current_archive = directory / "current.tar.gz"
        fallback_archive = directory / "fallback.tar.gz"
        _archive(current, current_archive)
        _archive(fallback, fallback_archive)
        current_restore = _extract(current_archive, directory / "current-restore")
        fallback_restore = _extract(fallback_archive, directory / "fallback-restore")
        current_sha = _sha256(current_archive)
        fallback_sha = _sha256(fallback_archive)
    return {
        "schemaVersion": "rac-v1-rollback-rehearsal.v0.1.0",
        "currentCommit": current,
        "fallbackTag": FALLBACK,
        "fallbackCommit": fallback,
        "artifacts": {
            "currentSourceArchiveSha256": current_sha,
            "fallbackSourceArchiveSha256": fallback_sha,
        },
        "restore": {
            "currentRequiredPaths": current_restore,
            "fallbackRequiredPaths": fallback_restore,
            "currentPass": len(current_restore) == len(REQUIRED_PATHS),
            "fallbackPass": len(fallback_restore) == len(REQUIRED_PATHS),
        },
        "tabletop": {
            "owner": "rac-maintainers",
            "trigger": "artifact integrity, security, or compatibility failure",
            "actions": [
                "freeze publication and preserve the failing artifact and logs",
                "announce the affected commit/tag and compatibility impact",
                "restore the last verified source/archive and compatibility metadata",
                "rerun the full local and hosted qualification gates",
                "publish a corrective release only after human approval",
            ],
            "externalActions": "Hosted yanking, package rollback, signing, and notification remain unperformed.",
        },
        "result": "pass"
        if len(current_restore) == len(REQUIRED_PATHS)
        and len(fallback_restore) == len(REQUIRED_PATHS)
        else "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report()
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
