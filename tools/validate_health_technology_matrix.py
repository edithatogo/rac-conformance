"""Validate health-technology authority boundaries and source states."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(root: Path) -> list[str]:
    matrix = json.loads((root / "authority-matrix.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    authorities = {
        authority["id"]: authority
        for jurisdiction in matrix.get("jurisdictions", [])
        for authority in jurisdiction.get("authorities", [])
    }
    required = {"medsafe", "pharmac", "tga", "pbac", "pbs", "msac", "mbs", "mhra", "nice", "fda", "cms"}
    missing = required - authorities.keys()
    if missing:
        errors.append(f"authority matrix missing: {sorted(missing)}")
    for rule in matrix.get("nonEquivalenceRules", []):
        forbidden = rule.get("forbid", {})
        authority = authorities.get(forbidden.get("authority"))
        if authority and forbidden.get("role") in authority.get("roles", []):
            errors.append(f"non-equivalence violated: {rule['id']}")
    if "market_authorisation" in authorities["fda"].get("roles", []) and "payer_coverage" in authorities["fda"].get("roles", []):
        errors.append("FDA cannot be both regulator and payer")
    if "market_authorisation" in authorities["mbs"].get("roles", []):
        errors.append("MBS cannot be a medicine regulator")

    manifest = json.loads((root / "sources/manifest.json").read_text(encoding="utf-8"))
    source_ids = {source["id"] for source in manifest.get("sources", [])}
    for source in manifest.get("sources", []):
        if source["verificationStatus"] == "observed" and not source.get("url"):
            errors.append(f"observed source has no URL: {source['id']}")
        if source["verificationStatus"] in {"blocked", "UNVERIFIED"} and source.get("digest"):
            errors.append(f"blocked/unverified source cannot have digest: {source['id']}")
    for authority in authorities.values():
        if not any(source["authority"] == authority["id"] for source in manifest["sources"]):
            errors.append(f"authority has no source assertion: {authority['id']}")
    if len(source_ids) != len(manifest.get("sources", [])):
        errors.append("source IDs must be unique")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default="subrepos/process-mappings/profiles/health-technology")
    args = parser.parse_args()
    errors = validate(Path(args.root))
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("OK: health-technology authority matrix and source manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
