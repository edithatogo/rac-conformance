"""Generate deterministic manuscript summary tables from committed JSONL evidence."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def summary(path: Path, title: str) -> str:
    rows = read_jsonl(path)
    classifications = Counter(row.get("classification", row.get("status", "unknown")) for row in rows)
    agreements = sum(1 for row in rows if row.get("agreement") is True)
    lines = [
        f"# {title}",
        "",
        f"Source: `{path.relative_to(ROOT)}`",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {len(rows)} |",
        f"| Agreements | {agreements} |",
        "",
        "| Classification | Cases |",
        "|---|---:|",
    ]
    lines.extend(f"| `{key}` | {classifications[key]} |" for key in sorted(classifications))
    return "\n".join(lines) + "\n"


TARGETS = {
    ROOT / "studies/nz-reconciliation/paper/ARTIFACT_SUMMARY.md": (
        ROOT / "studies/nz-reconciliation/results/comparison-live-results.jsonl",
        "NZ reconciliation artifact summary",
    ),
    ROOT / "studies/snap-divergence/paper/ARTIFACT_SUMMARY.md": (
        ROOT / "studies/snap-divergence/results/comparison-approved-results.jsonl",
        "SNAP approved comparison artifact summary",
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")
    failures = []
    for target, (source, title) in TARGETS.items():
        expected = summary(source, title)
        if args.write:
            target.write_text(expected, encoding="utf-8")
        elif not target.exists() or target.read_text(encoding="utf-8") != expected:
            failures.append(str(target.relative_to(ROOT)))
    if failures:
        print("stale paper artifacts: " + ", ".join(failures))
        return 1
    print("paper artifacts passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
