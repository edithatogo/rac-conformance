"""Project PolicyEngine flat traces into PIC trace documents."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

TRACE_KEY_RE = re.compile(r"^(?P<name>.+)<(?P<period>[^<>]+), \((?P<branch>[^()]*)\)>$")


@dataclass(frozen=True)
class ParsedKey:
    raw: str
    name: str
    period: str
    branch: str


def project_flat_trace(
    flat_trace: Mapping[str, Mapping[str, Any]],
    *,
    output_key: str,
    case_id: str,
    package_id: str,
    package_version: str,
    engine_version: str,
    timestamp: str,
    namespace: str = "policyengine-us",
    adapter: str = "policyengine-flat-trace-prototype",
    money_variables: frozenset[str] = frozenset({"snap"}),
) -> dict[str, Any]:
    """Project a PolicyEngine serialized flat trace to `pic-traces/0.1.0`.

    `flat_trace` is the dict returned by
    `sim.tracer.get_serialized_flat_trace()`. The resulting steps are ordered
    dependency-first for the requested output node.
    """

    if output_key not in flat_trace:
        raise KeyError(f"output key not found in flat trace: {output_key}")

    ordered_keys = _dependency_order(flat_trace, output_key)
    parsed_output = parse_trace_key(output_key)
    output_id = _variable_id(namespace, parsed_output.name, category="decision")

    steps = [
        _project_step(
            flat_trace,
            key,
            namespace=namespace,
            money_variables=money_variables,
        )
        for key in ordered_keys
    ]

    return {
        "conformsTo": "pic-traces/0.1.0",
        "caseId": case_id,
        "packageRef": {"id": package_id, "version": package_version},
        "engine": {
            "name": "policyengine-us",
            "version": engine_version,
            "adapter": adapter,
        },
        "timestamp": timestamp,
        "inputs": _project_inputs(flat_trace, ordered_keys, namespace=namespace),
        "outputs": {
            output_id: _value_object(
                flat_trace[output_key].get("value"),
                is_money=parsed_output.name in money_variables,
            ),
        },
        "steps": steps,
    }


def parse_trace_key(key: str) -> ParsedKey:
    match = TRACE_KEY_RE.match(key)
    if not match:
        raise ValueError(f"invalid PolicyEngine trace key: {key}")
    return ParsedKey(
        raw=key,
        name=match.group("name"),
        period=match.group("period").strip(),
        branch=match.group("branch").strip(),
    )


def _dependency_order(
    flat_trace: Mapping[str, Mapping[str, Any]],
    output_key: str,
) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []

    def visit(key: str) -> None:
        if key in seen:
            return
        seen.add(key)
        for dependency in flat_trace.get(key, {}).get("dependencies", []):
            if dependency in flat_trace:
                visit(dependency)
        ordered.append(key)

    visit(output_key)
    return ordered


def _project_step(
    flat_trace: Mapping[str, Mapping[str, Any]],
    key: str,
    *,
    namespace: str,
    money_variables: frozenset[str],
) -> dict[str, Any]:
    parsed = parse_trace_key(key)
    node = flat_trace[key]
    result_id = _variable_id(namespace, parsed.name, category="decision")

    parameters = node.get("parameters", {})
    parameter_versions = []
    for parameter_key in sorted(parameters):
        parsed_param = parse_trace_key(parameter_key)
        parameter_versions.append({
            "id": _variable_id(namespace, parsed_param.name, category="parameter"),
            "effectiveFrom": _effective_from(parsed_param.period),
        })

    dependencies = node.get("dependencies", [])
    inputs_used = []
    for dependency in dependencies:
        parsed_dep = parse_trace_key(dependency)
        inputs_used.append(_variable_id(namespace, parsed_dep.name, category="decision"))

    return {
        "stepId": _step_id(parsed),
        "kind": "decision",
        "refs": {"decision": result_id},
        "inputsUsed": inputs_used,
        "parameterVersions": parameter_versions,
        "result": _value_object(
            node.get("value"),
            is_money=parsed.name in money_variables,
        ),
        "sourceRefs": [f"PolicyEngine flat trace node: {key}"],
    }


def _project_inputs(
    flat_trace: Mapping[str, Mapping[str, Any]],
    ordered_keys: list[str],
    *,
    namespace: str,
) -> dict[str, Any]:
    inputs: dict[str, Any] = {}
    for key in ordered_keys:
        node = flat_trace[key]
        if node.get("dependencies") or node.get("parameters"):
            continue
        parsed = parse_trace_key(key)
        inputs[_variable_id(namespace, parsed.name, category="variable")] = _value_object(
            node.get("value"),
            is_money=False,
        )
    return inputs


def _value_object(value: Any, *, is_money: bool) -> dict[str, Any]:
    value = _unwrap_singleton(value)
    if value is None:
        return {"valueState": "unknown"}
    if is_money:
        return {"value": _decimal_string(value), "valueState": "known", "currency": "USD"}
    if isinstance(value, bool):
        return {"value": value, "valueState": "known"}
    if isinstance(value, int):
        return {"value": value, "valueState": "known"}
    if isinstance(value, float):
        return {"value": _decimal_string(value), "valueState": "known"}
    if isinstance(value, str):
        return {"value": value, "valueState": "known"}
    return {"value": json.dumps(value, sort_keys=True), "valueState": "known"}


def _unwrap_singleton(value: Any) -> Any:
    if isinstance(value, list) and len(value) == 1:
        return value[0]
    return value


def _decimal_string(value: Any) -> str:
    decimal = Decimal(str(value))
    return format(decimal, "f")


def _variable_id(namespace: str, name: str, *, category: str) -> str:
    return f"{_namespace_slug(namespace)}/{category}.{_slug(name)}"


def _step_id(parsed: ParsedKey) -> str:
    return f"{_slug(parsed.name)}__{_slug(parsed.period)}__{_slug(parsed.branch)}"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")
    return slug or "unnamed"


def _namespace_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_-]+", "_", value.lower()).strip("_-")
    return slug or "namespace"


def _effective_from(period: str) -> str:
    if re.fullmatch(r"\d{4}", period):
        return f"{period}-01-01"
    if re.fullmatch(r"\d{4}-\d{2}", period):
        return f"{period}-01"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", period):
        return period
    return "1900-01-01"
