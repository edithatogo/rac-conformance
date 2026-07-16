import json
import random
from pathlib import Path

import pytest

from pic_contracts.safety import SafetyLimitError, load_bounded_json


def test_seeded_bounded_json_corpus_round_trips_deterministically(tmp_path: Path) -> None:
    generator = random.Random(20260716)
    for index in range(25):
        document = {
            "case": index,
            "values": [generator.randint(0, 1000) for _ in range(index % 7)],
            "state": "known" if index % 2 else "unknown",
        }
        path = tmp_path / f"case-{index}.json"
        path.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
        assert load_bounded_json(path) == load_bounded_json(path)


def test_seeded_hostile_strings_are_bounded(tmp_path: Path) -> None:
    path = tmp_path / "hostile.json"
    path.write_text(json.dumps({"value": "line\nquote\\" * 100}), encoding="utf-8")
    with pytest.raises(SafetyLimitError, match="max_string_bytes"):
        load_bounded_json(path, max_string_bytes=20)
