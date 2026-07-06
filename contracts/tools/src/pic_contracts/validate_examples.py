"""Validate contract example corpora."""

from __future__ import annotations

import argparse
from pathlib import Path

from pic_contracts.validation import ValidationIssue, ValidationReport, validate_file


def validate_example_corpus(root: Path) -> ValidationReport:
    report = ValidationReport()
    for valid_path in sorted(root.glob("pic-*/*/examples/valid/*.json")):
        result = validate_file(valid_path)
        if not result.ok:
            report.extend(result.issues)
    for invalid_path in sorted(root.glob("pic-*/*/examples/invalid/*.json")):
        result = validate_file(invalid_path)
        if result.ok:
            report.add(
                ValidationIssue(
                    str(invalid_path),
                    "invalid example unexpectedly passed validation",
                    "negative-test",
                )
            )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PIC example corpora")
    parser.add_argument("root", nargs="?", default="../../contracts")
    args = parser.parse_args(argv)
    report = validate_example_corpus(Path(args.root))
    if report.ok:
        print(f"OK: example corpus under {args.root}")
        return 0
    for issue in report.issues:
        print(f"{issue.code}: {issue.path}: {issue.message}")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

