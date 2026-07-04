# Draft PolicyEngine Issue: Versioned trace export

Target repository: `PolicyEngine/policyengine-core`

Suggested title:

`Proposal: versioned computation trace export for household calculations`

## Draft body

I have been testing PolicyEngine's existing tracing machinery for downstream audit and conformance workflows. The current `FullTracer`/`FlatTrace` API already exposes the core information needed for a deterministic trace export: calculation nodes, dependencies, parameter reads, values, branches, periods, and timings.

I would like to propose a small, versioned export API over the existing trace data, for example:

```python
sim = Simulation(situation=situation, trace=True)
sim.calculate("snap", "2024-01")
trace = sim.tracer.to_trace(format="policyengine.trace.v1")
```

Minimum useful fields:

- `format`: a stable format/version string, such as `policyengine.trace.v1`
- `engine`: `policyengine-core` version, model package name/version, and optionally git revision
- `calculation`: requested variable, period, branch, and entity/count metadata
- `nodes`: dependency-ordered calculation nodes with `id`, `variable`, `period`, `branch`, `dependencies`, `parameters`, `value`, and optional timing fields
- `parameters`: accessed parameter names, instants/effective dates, scalar/vector values or summaries, and source/version metadata where available

Why this may be useful:

- Audit trails for household-level calculations.
- Debugging and reproducible explanation of why a calculation changed.
- Cross-engine comparison where result equality is not enough and users need to compare calculation paths.
- Downstream documentation or conformance formats without requiring PolicyEngine to adopt those formats directly.

Local evidence from a SNAP household calculation:

- `policyengine-core==3.28.0`
- `policyengine-us==1.755.5`
- `policyengine-core` revision: `f761573c2a13adecc3826be04af1980d13657e1d`
- `policyengine-us` revision: `fc64cef64ab55c3c48309c7fb304c35e5f3c9184`
- Household SNAP result: `snap [291.0]`
- Trace shape: one root tree, 2,833 serialized flat-trace nodes
- Root dependencies: `takes_up_snap_if_eligible`, `snap_normal_allotment`, `snap_emergency_allotment`, and `dc_snap_temporary_local_benefit`

I also built a small external prototype that projects the current `sim.tracer.get_serialized_flat_trace()` dict into a dependency-ordered trace document. That prototype validates a projected SNAP trace with 2,833 steps and 164 inferred leaf inputs against a downstream JSON Schema. The prototype is evidence that the existing tracer already has enough structure for a stable export; it is not a request that PolicyEngine support that downstream schema.

Questions for maintainers:

1. Would a versioned `FullTracer.to_trace()` or `Simulation.to_trace()` helper be welcome in `policyengine-core`?
2. Should this live as a JSON-compatible export only, or should PolicyEngine expose a typed Python dataclass layer first?
3. What model/package version metadata should be considered stable enough for a trace export?
4. Is parameter source/version metadata available today in a form maintainers would be comfortable exposing?

Scope intentionally not proposed here:

- No runtime AI or explanation generation.
- No replacement for PolicyEngine's native formulas or tests.
- No normative external schema dependency.
- No promise that microsimulation traces are cheap enough for population-scale use. Direct `policyengine-us` microsimulation is now described as deprecated in favour of the managed `policyengine.py` bundle, and I did not measure a 1,000-household CPS sample without first agreeing on remote dataset access and a pinned dataset revision.

## Local evidence files

- `external/policyengine/TRACE_INVESTIGATION.md`
- `harness/policyengine_trace/projection.py`
- `harness/tests/test_policyengine_trace_projection.py`
- `Makefile` targets `harness-lint` and `harness-test`

## Validation run

```text
make check
```

Green locally after adding the prototype harness.

Additional live integration run, using the local editable PolicyEngine venv and the same SNAP household:

```text
validated 2833 steps 164 inputs {'us-snap/decision.snap': {'value': '291.0', 'valueState': 'known', 'currency': 'USD'}}
```

Footnote: the downstream schema used for the prototype is a local "PIC traces" schema for policy interoperability conformance work. It is deliberately kept outside the proposed PolicyEngine API shape.
