"""Fail-closed intake validation for the upstream FOI-O release bundle."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SHA = re.compile(r"^[0-9a-fA-F]{40}$")
REQUIRED = {
    "release",
    "capabilities",
    "contracts",
    "migrations",
    "tests",
    "fixtures",
    "provenance",
    "empiricalResults",
    "exceptions",
    "limitations",
}


def validate(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    release = bundle.get("release")
    if not isinstance(release, dict):
        errors.append("release: required object")
    else:
        if not isinstance(release.get("tag"), str) or not release["tag"].startswith("v"):
            errors.append("release.tag: required version tag")
        if not isinstance(release.get("commit"), str) or not SHA.fullmatch(release["commit"]):
            errors.append("release.commit: required 40-character commit SHA")
    missing = sorted(REQUIRED - bundle.keys())
    errors.extend(f"{name}: required" for name in missing)
    for name in REQUIRED - {"release"}:
        if name in bundle and not isinstance(bundle[name], (list, dict)):
            errors.append(f"{name}: must be an array or object")
    provenance = bundle.get("provenance")
    if isinstance(provenance, dict) and provenance.get("status") in {"dirty", "unknown", "unverified"}:
        errors.append("provenance.status: must be verified")
    return sorted(errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args(argv)
    try:
        value = json.loads(args.bundle.read_text(encoding="utf-8"))
        errors = validate(value) if isinstance(value, dict) else ["root: required object"]
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"input: {exc}"]
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
