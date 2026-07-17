"""Validate candidate health-technology profiles and their promotion boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pic_contracts.health_profiles import validate_candidate_document
from pic_contracts.validation import validate_file


def validate_candidate(path: Path) -> list[str]:
    errors = [issue.message for issue in validate_file(path).issues]
    if errors:
        return errors
    document = json.loads(path.read_text(encoding="utf-8"))
    return validate_candidate_document(document)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    for path in args.paths:
        errors.extend(f"{path}: {error}" for error in validate_candidate(path))
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
