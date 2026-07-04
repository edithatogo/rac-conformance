"""Deterministic OpenFisca/PolicyEngine/PIC fixture conversion."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Literal

import yaml

Dialect = Literal["openfisca", "policyengine"]

UNSUPPORTED_FIELDS = {
    "relative_error_margin",
    "keywords",
    "ignore_variables",
    "only_variables",
    "reforms",
    "extensions",
    "parameters",
    "max_spiral_loops",
}

ENGINE_ALLOWED_FIELDS = {
    "openfisca": {
        "absolute_error_margin",
        "description",
        "extensions",
        "ignore_variables",
        "input",
        "keywords",
        "max_spiral_loops",
        "name",
        "only_variables",
        "output",
        "period",
        "parameters",
        "reforms",
        "relative_error_margin",
    },
    "policyengine": {
        "absolute_error_margin",
        "description",
        "extensions",
        "ignore_variables",
        "input",
        "keywords",
        "name",
        "only_variables",
        "output",
        "period",
        "reforms",
        "relative_error_margin",
    },
}


class UnsupportedConstructError(ValueError):
    """Raised when an engine test uses a construct outside the v0.1 subset."""

    def __init__(self, construct: str, *, source: str | None = None) -> None:
        self.construct = construct
        self.source = source
        prefix = f"{source}: " if source else ""
        super().__init__(f"{prefix}unsupported construct: {construct}")


@dataclass(frozen=True)
class Crosswalk:
    by_native: dict[str, str]
    by_pic: dict[str, str]


def openfisca_to_pic(source: str | Path | dict[str, Any] | list[Any], *, crosswalk=None) -> list[dict]:
    return _engine_to_pic(source, dialect="openfisca", crosswalk=crosswalk)


def policyengine_to_pic(source: str | Path | dict[str, Any] | list[Any], *, crosswalk=None) -> list[dict]:
    return _engine_to_pic(source, dialect="policyengine", crosswalk=crosswalk)


def pic_to_openfisca(fixture: dict[str, Any], *, crosswalk=None) -> list[dict[str, Any]]:
    return _pic_to_engine(fixture, dialect="openfisca", crosswalk=crosswalk)


def pic_to_policyengine(fixture: dict[str, Any], *, crosswalk=None) -> list[dict[str, Any]]:
    return _pic_to_engine(fixture, dialect="policyengine", crosswalk=crosswalk)


def _engine_to_pic(
    source: str | Path | dict[str, Any] | list[Any],
    *,
    dialect: Dialect,
    crosswalk,
) -> list[dict]:
    source_label, docs = _load_engine_docs(source)
    walk = _load_crosswalk(crosswalk, dialect)
    cases = [
        _case_to_pic(case, dialect=dialect, index=index, source=source_label, crosswalk=walk)
        for index, case in enumerate(docs, start=1)
    ]
    return [
        {
            "conformsTo": "pic-fixtures/0.1.0",
            "provenance": {
                "curator": "pic-fixture-converters",
                "method": "mechanical",
                "source": source_label or f"native:{dialect}",
                "interpreterOfRecord": "source engine fixture",
                "disclaimer": "Mechanical format conversion only; fixture meaning remains with the source project.",
                "notes": f"idScheme=native:{dialect}; crosswalk={'yes' if walk else 'no'}",
            },
            "cases": cases,
        }
    ]


def _pic_to_engine(fixture: dict[str, Any], *, dialect: Dialect, crosswalk) -> list[dict[str, Any]]:
    walk = _load_crosswalk(crosswalk, dialect)
    return [_pic_case_to_engine(case, dialect=dialect, crosswalk=walk) for case in fixture["cases"]]


def _load_engine_docs(source: str | Path | dict[str, Any] | list[Any]) -> tuple[str | None, list[dict]]:
    if isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
        path = Path(source)
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        source_label = str(path)
    else:
        data = source
        source_label = None
    docs = data if isinstance(data, list) else [data]
    if not all(isinstance(item, dict) for item in docs):
        raise UnsupportedConstructError("non_mapping_yaml_test", source=source_label)
    return source_label, docs


def _case_to_pic(
    case: dict[str, Any],
    *,
    dialect: Dialect,
    index: int,
    source: str | None,
    crosswalk: Crosswalk | None,
) -> dict[str, Any]:
    _check_supported_top_level(case, dialect=dialect, source=source)
    if not case.get("period"):
        raise UnsupportedConstructError("missing_period", source=source)
    if not case.get("output"):
        raise UnsupportedConstructError("missing_output", source=source)
    if dialect == "policyengine":
        dotted = [key for key in (case.get("input") or {}) if "." in str(key)]
        if dotted:
            raise UnsupportedConstructError(f"dotted_input_key:{dotted[0]}", source=source)

    id_map: dict[str, str] = {}
    input_paths: dict[str, list[str]] = {}
    output_paths: dict[str, list[str]] = {}
    inputs: dict[str, dict[str, Any]] = {}
    expected: dict[str, dict[str, Any]] = {}
    tolerance = _normalise_tolerance(case.get("absolute_error_margin"), dialect=dialect, source=source)

    for path, value in _flatten(case.get("input") or {}, source=source):
        native_name = path[-1]
        pic_id = _pic_id(native_name, dialect=dialect, crosswalk=crosswalk)
        unique_id = _unique_id(pic_id, path, id_map)
        id_map[unique_id] = native_name
        input_paths[unique_id] = list(path)
        inputs[unique_id] = _value_object(value, source=source)

    for path, value in _flatten(case["output"], source=source):
        native_name = path[-1]
        pic_id = _pic_id(native_name, dialect=dialect, crosswalk=crosswalk)
        unique_id = _unique_id(pic_id, path, id_map)
        id_map[unique_id] = native_name
        output_paths[unique_id] = list(path)
        item = _expected_value(value, source=source)
        applied_tolerance = _tolerance_for(tolerance, native_name)
        if applied_tolerance is not None:
            item["tolerance"] = applied_tolerance
        expected[unique_id] = item

    name = str(case.get("name") or f"{dialect} case {index}")
    description = str(case.get("description") or name)
    return {
        "caseId": f"native/{dialect}/case.{_slug(name, fallback=str(index))}",
        "description": description,
        "period": str(case["period"]),
        "entities": {
            "_pic_fixture_converters": {
                "dialect": dialect,
                "caseName": name,
                "idMap": id_map,
                "inputPaths": input_paths,
                "outputPaths": output_paths,
            }
        },
        "inputs": inputs,
        "expected": expected,
        "sourceRefs": [source or f"native:{dialect}"],
    }


def _pic_case_to_engine(
    case: dict[str, Any],
    *,
    dialect: Dialect,
    crosswalk: Crosswalk | None,
) -> dict[str, Any]:
    meta = case.get("entities", {}).get("_pic_fixture_converters", {})
    id_map = dict(meta.get("idMap") or {})
    input_paths = dict(meta.get("inputPaths") or {})
    output_paths = dict(meta.get("outputPaths") or {})
    out: dict[str, Any] = {"name": meta.get("caseName") or case["description"], "period": case["period"]}
    inputs: dict[str, Any] = {}
    outputs: dict[str, Any] = {}
    for pic_id, value_obj in case.get("inputs", {}).items():
        path = input_paths.get(pic_id) or [_native_name(pic_id, id_map, crosswalk)]
        _assign_path(inputs, path, _engine_value(value_obj))
    for pic_id, expected_obj in case.get("expected", {}).items():
        path = output_paths.get(pic_id) or [_native_name(pic_id, id_map, crosswalk)]
        _assign_path(outputs, path, _engine_value(expected_obj))
    if inputs:
        out["input"] = inputs
    out["output"] = outputs
    tolerance = _first_tolerance(case.get("expected", {}))
    if tolerance is not None:
        out["absolute_error_margin"] = _engine_number(tolerance)
    return out


def _check_supported_top_level(case: dict[str, Any], *, dialect: Dialect, source: str | None) -> None:
    for key in case:
        if key not in ENGINE_ALLOWED_FIELDS[dialect]:
            raise UnsupportedConstructError(f"unexpected_field:{key}", source=source)
        if key in UNSUPPORTED_FIELDS:
            raise UnsupportedConstructError(key, source=source)


def _flatten(value: Any, *, source: str | None, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    if isinstance(value, dict):
        leaves: list[tuple[tuple[str, ...], Any]] = []
        for key, child in value.items():
            leaves.extend(_flatten(child, source=source, path=(*path, str(key))))
        return leaves
    _check_scalar(value, source=source)
    return [(path, value)]


def _check_scalar(value: Any, *, source: str | None) -> None:
    if value is None:
        raise UnsupportedConstructError("null_value", source=source)
    if isinstance(value, list):
        raise UnsupportedConstructError("list_value", source=source)
    if isinstance(value, str) and _looks_like_expression(value):
        raise UnsupportedConstructError("expression_string", source=source)
    if not isinstance(value, bool | int | float | str):
        raise UnsupportedConstructError(type(value).__name__, source=source)


def _looks_like_expression(value: str) -> bool:
    return bool(re.search(r"\d", value) and re.search(r"[()+*/]", value))


def _value_object(value: Any, *, source: str | None) -> dict[str, Any]:
    _check_scalar(value, source=source)
    return {"value": _pic_value(value), "valueState": "known", "epistemicStatus": "observed"}


def _expected_value(value: Any, *, source: str | None) -> dict[str, Any]:
    _check_scalar(value, source=source)
    return {"value": _pic_value(value), "valueState": "known", "epistemicStatus": "asserted"}


def _pic_value(value: bool | int | float | str) -> bool | int | str:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return _decimal_string(value)
    return value


def _engine_value(value_obj: dict[str, Any]) -> Any:
    value = value_obj.get("value")
    if isinstance(value, str) and _is_decimal_string(value):
        return _engine_number(value)
    return value


def _decimal_string(value: Any) -> str:
    try:
        decimal = Decimal(str(value))
    except InvalidOperation as exc:
        raise UnsupportedConstructError(f"non_decimal:{value}") from exc
    return format(decimal, "f")


def _is_decimal_string(value: str) -> bool:
    try:
        Decimal(value)
    except InvalidOperation:
        return False
    return bool(re.fullmatch(r"-?[0-9]+(\.[0-9]+)?", value))


def _engine_number(value: str) -> int | float:
    decimal = Decimal(value)
    if decimal == decimal.to_integral_value() and "." not in value:
        return int(decimal)
    return float(decimal)


def _normalise_tolerance(value: Any, *, dialect: Dialect, source: str | None) -> str | dict[str, str] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        if dialect == "policyengine":
            raise UnsupportedConstructError("absolute_error_margin_mapping", source=source)
        return {str(key): _decimal_string(item) for key, item in value.items()}
    if isinstance(value, bool | list):
        raise UnsupportedConstructError("absolute_error_margin", source=source)
    return _decimal_string(value)


def _tolerance_for(tolerance: str | dict[str, str] | None, variable: str) -> str | None:
    if isinstance(tolerance, dict):
        return tolerance.get(variable) or tolerance.get("default")
    return tolerance


def _first_tolerance(expected: dict[str, dict[str, Any]]) -> str | None:
    values = {item["tolerance"] for item in expected.values() if "tolerance" in item}
    return values.pop() if len(values) == 1 else None


def _pic_id(native_name: str, *, dialect: Dialect, crosswalk: Crosswalk | None) -> str:
    if crosswalk is not None:
        try:
            return crosswalk.by_native[native_name]
        except KeyError as exc:
            raise UnsupportedConstructError(f"missing_crosswalk_mapping:{native_name}") from exc
    return f"native/{dialect}/{_slug(native_name)}.value"


def _unique_id(pic_id: str, path: tuple[str, ...], id_map: dict[str, str]) -> str:
    if pic_id not in id_map:
        return pic_id
    digest = hashlib.sha1("/".join(path).encode("utf-8")).hexdigest()[:8]
    base, suffix = pic_id.rsplit(".", 1)
    return f"{base}_{digest}.{suffix}"


def _native_name(pic_id: str, id_map: dict[str, str], crosswalk: Crosswalk | None) -> str:
    if pic_id in id_map:
        return id_map[pic_id]
    if crosswalk is not None and pic_id in crosswalk.by_pic:
        return crosswalk.by_pic[pic_id]
    return pic_id.rsplit("/", 1)[-1].rsplit(".", 1)[0]


def _assign_path(target: dict[str, Any], path: list[str], value: Any) -> None:
    current = target
    for key in path[:-1]:
        current = current.setdefault(key, {})
    current[path[-1]] = value


def _slug(value: str, fallback: str = "item") -> str:
    slug = re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")
    return slug or fallback


def _load_crosswalk(crosswalk, dialect: Dialect) -> Crosswalk | None:
    if crosswalk is None:
        return None
    if isinstance(crosswalk, Path) or (isinstance(crosswalk, str) and Path(crosswalk).exists()):
        doc = json.loads(Path(crosswalk).read_text(encoding="utf-8"))
    else:
        doc = crosswalk
    by_native: dict[str, str] = {}
    by_pic: dict[str, str] = {}
    for row in doc.get("rows", []):
        pic_id = row["id"]
        for mapping in row.get("mappings", []):
            if mapping.get("system") == dialect:
                native = mapping["ref"]
                by_native[native] = pic_id
                by_pic[pic_id] = native
    return Crosswalk(by_native=by_native, by_pic=by_pic)
