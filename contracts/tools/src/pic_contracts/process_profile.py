"""Deterministic projections for PIC process-profile traces."""

from __future__ import annotations

from datetime import datetime
from typing import Any


def normalize_trace(profile: dict[str, Any], trace_id: str) -> dict[str, Any]:
    """Return a stable, platform-neutral projection of one profile trace."""
    traces = {trace["id"]: trace for trace in profile["traces"]}
    trace = traces[trace_id]
    events = {event["id"]: event for event in profile["events"]}
    invocations = {item["id"]: item for item in profile["ruleInvocations"]}

    def event_key(event: dict[str, Any]) -> tuple[datetime, str]:
        return datetime.fromisoformat(event["occurredAt"].replace("Z", "+00:00")), event["id"]

    return {
        "traceId": trace["id"],
        "traceContract": trace["traceContract"],
        "equivalenceClaim": trace["equivalenceClaim"],
        "events": [
            {
                "id": event["id"],
                "kind": event["kind"],
                "eventType": event["eventType"],
                "occurredAt": event["occurredAt"],
            }
            for event in sorted((events[event_id] for event_id in trace["eventIds"]), key=event_key)
        ],
        "ruleInvocations": [
            {
                "id": invocations[item_id]["id"],
                "ruleId": invocations[item_id]["ruleId"],
                "fixtureRef": invocations[item_id]["fixtureRef"],
                "parameterRefs": sorted(invocations[item_id]["parameterRefs"]),
                "traceId": invocations[item_id]["traceId"],
            }
            for item_id in sorted(trace["ruleInvocationIds"])
        ],
        "lossNotes": sorted(trace.get("lossNotes", [])),
    }
