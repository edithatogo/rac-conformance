"""Produce reproducible source-archive and provenance evidence."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _archive(commit: str, destination: Path) -> None:
    tar_path = destination.with_suffix(".tar")
    with tar_path.open("wb") as stream:
        subprocess.run(
            ["git", "archive", "--format=tar", "--prefix=rac-conformance/", commit],
            cwd=ROOT,
            check=True,
            stdout=stream,
        )
    with tar_path.open("rb") as source, destination.open("wb") as output, gzip.GzipFile(
        filename="", fileobj=output, mode="wb", mtime=0
    ) as compressed:
        compressed.write(source.read())
    tar_path.unlink()


def build_report() -> dict[str, object]:
    commit = _git("rev-parse", "HEAD")
    tree = _git("rev-parse", "HEAD^{tree}")
    with tempfile.TemporaryDirectory(prefix="rac-v1-repro-") as temporary:
        directory = Path(temporary)
        first = directory / "first.tar.gz"
        second = directory / "second.tar.gz"
        _archive(commit, first)
        _archive(commit, second)
        first_sha = _sha256(first)
        second_sha = _sha256(second)
    sbom = ROOT / "docs/V1_SBOM.json"
    return {
        "schemaVersion": "rac-v1-reproducibility.v0.1.0",
        "commit": commit,
        "tree": tree,
        "sourceArchive": {
            "firstSha256": first_sha,
            "secondSha256": second_sha,
            "identical": first_sha == second_sha,
        },
        "trackedEvidence": {
            "sbom": _sha256(sbom) if sbom.exists() else None,
            "threatModel": _sha256(ROOT / "docs/V1_THREAT_MODEL.md"),
            "riskRegister": _sha256(ROOT / "docs/V1_RISK_REGISTER.json"),
        },
        "hostedAttestation": "not-performed; requires GitHub release workflow and human signing authorization",
        "result": "pass" if first_sha == second_sha else "fail",
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
