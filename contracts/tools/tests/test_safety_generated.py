"""Bounded generated inputs for the production PIC JSON resource guards.

These are synthetic contract properties, not promoted policy/golden fixtures.
Every failure identifies its deterministic parameter tuple in pytest output.
"""

import json
from pathlib import Path

import pytest

from pic_contracts.safety import SafetyLimitError, load_bounded_json


@pytest.mark.parametrize("character", ["a", "é", "中", "🧬", "\\", "\0", '"', "~", "/"])
@pytest.mark.parametrize("count", [1, 2, 7, 31, 64])
@pytest.mark.parametrize("location", ["key", "value", "list"])
@pytest.mark.parametrize("ensure_ascii", [False, True])
def test_utf8_string_limit_is_exact_at_every_location(
    tmp_path: Path, character: str, count: int, location: str, ensure_ascii: bool
) -> None:
    text = character * count
    if location == "key":
        document = {text: None}
    elif location == "list":
        document = {"k": [text]}
    else:
        document = {"k": text}
    path = tmp_path / "string.json"
    path.write_text(json.dumps(document, ensure_ascii=ensure_ascii), encoding="utf-8")
    byte_count = len(text.encode("utf-8"))
    assert load_bounded_json(path, max_string_bytes=byte_count) == document
    assert load_bounded_json(path, max_string_bytes=byte_count + 1) == document
    with pytest.raises(SafetyLimitError, match="max_string_bytes"):
        load_bounded_json(path, max_string_bytes=byte_count - 1)


@pytest.mark.parametrize("depth", range(1, 33))
@pytest.mark.parametrize("alternating_lists", [False, True])
def test_depth_boundary_counts_objects_lists_and_scalar_leaves(
    tmp_path: Path, depth: int, alternating_lists: bool
) -> None:
    nested = 0
    for layer in range(depth - 1):
        nested = [nested] if alternating_lists and layer % 2 else {"k": nested}
    document = {"k": nested}
    path = tmp_path / "depth.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    assert load_bounded_json(path, max_depth=depth) == document
    assert load_bounded_json(path, max_depth=depth + 1) == document
    with pytest.raises(SafetyLimitError, match="max_depth"):
        load_bounded_json(path, max_depth=depth - 1)


@pytest.mark.parametrize("padding", range(0, 65, 4))
@pytest.mark.parametrize("ensure_ascii", [False, True])
def test_input_byte_boundary_includes_encoding_and_json_whitespace(
    tmp_path: Path, padding: int, ensure_ascii: bool
) -> None:
    document = {"µ": [None, True, False, -17, 2**64, "🧬" * padding]}
    raw = (" " * padding + json.dumps(document, ensure_ascii=ensure_ascii) + "\n").encode()
    path = tmp_path / "size.json"
    path.write_bytes(raw)
    assert load_bounded_json(path, max_bytes=len(raw)) == document
    assert load_bounded_json(path, max_bytes=len(raw) + 1) == document
    with pytest.raises(SafetyLimitError, match="max_bytes"):
        load_bounded_json(path, max_bytes=len(raw) - 1)


@pytest.mark.parametrize("root", [None, True, False, 0, -1, 2**64, "text", [], [0], [{"k": 1}]])
def test_nonobject_roots_never_bypass_artifact_shape_guard(tmp_path: Path, root: object) -> None:
    path = tmp_path / "root.json"
    path.write_text(json.dumps(root), encoding="utf-8")
    with pytest.raises(SafetyLimitError, match="JSON object"):
        load_bounded_json(path)


def test_every_truncated_prefix_of_synthetic_json_is_rejected(tmp_path: Path) -> None:
    raw = json.dumps({"µ": [1, True, None, {"🧬": "line\nbreak"}]}, ensure_ascii=False).encode()
    path = tmp_path / "truncated.json"
    for end in range(len(raw)):
        path.write_bytes(raw[:end])
        with pytest.raises((json.JSONDecodeError, UnicodeDecodeError)):
            load_bounded_json(path)
    path.write_bytes(raw)
    assert load_bounded_json(path) == json.loads(raw)
