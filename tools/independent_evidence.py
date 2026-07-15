#!/usr/bin/env python3
"""Deterministically classify independent-validation evidence packets."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema is required to verify evidence packets") from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "conductor/tracks/v1_independent_validation_20260714/SUBMISSION_SCHEMA.json"
SHA256 = re.compile(r"^sha256:[0-9a-fA-F]{64}$")
OUTCOMES = {"qualifying", "partial", "conflicting", "withdrawn", "declined", "unresponsive"}
NON_QUALIFYING = {"internal-rehearsal", "unacknowledged", "maintainer-fork", "narrative-only"}


def classify(packet: dict, *, today: dt.date | None = None) -> dict:
    """Return a stable status and exception list without consulting the network."""
    schema = json.loads(SCHEMA.read_text())
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(packet), key=lambda e: list(e.path))
    exceptions = [f"schema: {error.message}" for error in errors]
    today = today or dt.date.today()

    if packet.get("independenceStatus") in NON_QUALIFYING:
        exceptions.append(f"non-qualifying independence status: {packet['independenceStatus']}")
    if packet.get("organisation", {}).get("controlRelationship") != "external":
        exceptions.append("organisation is not independently controlled")
    if packet.get("repository", {}).get("accessControl") != "external":
        exceptions.append("repository is not independently controlled")
    if packet.get("environment", {}).get("cleanCheckout") is not True:
        exceptions.append("execution was not from a clean checkout")
    if packet.get("acknowledgement", {}).get("status") != "confirmed":
        exceptions.append("external acknowledgement is missing")
    if packet.get("attestation", {}).get("issuerControl") != "external":
        exceptions.append("external owner attestation is missing")
    freshness = packet.get("maintenance", {}).get("freshnessDate")
    if freshness:
        try:
            age = (today - dt.date.fromisoformat(freshness)).days
            if age < 0 or age > 180:
                exceptions.append("maintenance evidence is stale or future-dated")
        except ValueError:
            pass
    if packet.get("testOutcome") != "pass":
        exceptions.append("test outcome is not pass")
    for field in ("sourceDigest", "inputDigest", "resultDigest"):
        if field in packet and not SHA256.fullmatch(packet[field]):
            exceptions.append(f"{field} is not a sha256 digest")

    declared = packet.get("independenceStatus")
    if declared in NON_QUALIFYING:
        status = "partial"
    elif declared not in OUTCOMES:
        status = "rejected"
    elif declared == "qualifying" and not exceptions:
        status = "qualifying"
    elif declared in {"conflicting", "withdrawn", "declined", "unresponsive"}:
        status = declared
    else:
        status = "partial"
    return {"status": status, "exceptions": sorted(set(exceptions)), "qualifiesForV1": status == "qualifying"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args(argv)
    try:
        packet = json.loads(args.packet.read_text())
        result = classify(packet)
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        result = {"status": "rejected", "exceptions": [f"input: {exc}"], "qualifiesForV1": False}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "qualifying" else 1


if __name__ == "__main__":
    sys.exit(main())
