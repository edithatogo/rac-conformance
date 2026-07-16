"""Resource bounds for untrusted JSON interchange artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SafetyLimitError(ValueError):
    """Raised when an input exceeds a deterministic parser safety limit."""


def _depth(value: Any, current: int = 0) -> int:
    if isinstance(value, dict):
        children = value.values()
    elif isinstance(value, list):
        children = value
    else:
        return current
    return max((_depth(item, current + 1) for item in children), default=current)


def load_bounded_json(
    path: Path,
    *,
    max_bytes: int = 4 * 1024 * 1024,
    max_depth: int = 64,
    max_string_bytes: int = 512 * 1024,
) -> dict[str, Any]:
    """Load an object while enforcing size, nesting, and string bounds."""
    raw = path.read_bytes()
    if len(raw) > max_bytes:
        raise SafetyLimitError(f"input exceeds max_bytes={max_bytes}")
    document = json.loads(raw.decode("utf-8"))
    if not isinstance(document, dict):
        raise SafetyLimitError("PIC artifact must be a JSON object")
    if _depth(document) > max_depth:
        raise SafetyLimitError(f"input exceeds max_depth={max_depth}")
    largest_string = max(
        (len(item.encode("utf-8")) for item in _strings(document)),
        default=0,
    )
    if largest_string > max_string_bytes:
        raise SafetyLimitError(f"input exceeds max_string_bytes={max_string_bytes}")
    return document


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _strings(key)
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)
