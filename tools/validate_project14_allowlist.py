"""Check an exported GitHub Project 14 item list against the FOI allowlist."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _item_key(item: dict[str, object]) -> str | None:
    content = item.get("content")
    if not isinstance(content, dict):
        return None
    repository = content.get("repository")
    number = content.get("number")
    if not isinstance(repository, str) or not isinstance(number, int):
        return None
    return f"{repository}#{number}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument(
        "--allowlist",
        type=Path,
        default=Path("conductor/tracks/foi_programme_governance_20260714/project14-allowlist.json"),
    )
    args = parser.parse_args()

    allowlist = json.loads(args.allowlist.read_text(encoding="utf-8"))
    export = json.loads(args.items.read_text(encoding="utf-8"))
    items = export.get("items", export)
    if not isinstance(items, list):
        raise ValueError("Project export must be a JSON list or an object with items")

    observed_by_key = {key: item for item in items if (key := _item_key(item))}
    observed = set(observed_by_key)
    required = set(allowlist["required_items"])
    expected_status = allowlist.get("expected_status")
    allowed_repositories = set(allowlist["allowed_repositories"])
    unrelated_repositories = sorted(
        key for key in observed if key.split("#", maxsplit=1)[0] not in allowed_repositories
    )
    extra_items = sorted(observed - required)
    missing = sorted(required - observed)
    stale = sorted(
        key
        for key in required & observed
        if expected_status and observed_by_key[key].get("status") != expected_status
    )

    print(f"observed={len(observed)} required={len(required)}")
    if missing:
        print("missing:")
        print("\n".join(f"- {key}" for key in missing))
    if unrelated_repositories:
        print("unrelated repositories:")
        print("\n".join(f"- {key}" for key in unrelated_repositories))
    if extra_items:
        print("extra items outside the exact FOI allowlist:")
        print("\n".join(f"- {key}" for key in extra_items))
    if stale:
        print(f"stale items (expected status: {expected_status}):")
        print("\n".join(f"- {key}" for key in stale))
    return 1 if missing or unrelated_repositories or extra_items or stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
