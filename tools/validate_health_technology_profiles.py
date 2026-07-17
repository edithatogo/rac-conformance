"""Validate candidate health-technology profiles and their promotion boundary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pic_contracts.validation import validate_file


def validate_candidate(path: Path) -> list[str]:
    errors = [issue.message for issue in validate_file(path).issues]
    if errors:
        return errors
    document = json.loads(path.read_text(encoding="utf-8"))
    if not document.get("profileId", "").startswith("health-technology/process."):
        errors.append("candidate profile must use the health-technology process namespace")
    for assertion in document["sourceAssertions"]:
        if assertion["controlling"] and not (
            assertion["sourceType"] == "official_primary"
            and assertion["reviewStatus"] in {"official-primary", "human-approved"}
        ):
            errors.append(
                f"controlling source assertion is not independently eligible: {assertion['id']}"
            )
    if any(trace["equivalenceClaim"] != "none" for trace in document["traces"]):
        errors.append("candidate traces must not claim equivalence")
    if not any(item["kind"] == "human_adjudication_required" for item in document.get("exceptions", [])):
        errors.append("candidate profile must retain a human adjudication exception")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    for path in args.paths:
        errors.extend(f"{path}: {error}" for error in validate_candidate(path))
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
