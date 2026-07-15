# v1 Normative Freeze

Status: release-candidate freeze proposal; v1.0 publication remains blocked by
the release-gate audit.

Freeze base: `f6df1e5` (the reviewed release-gate audit commit).

## Normative surface

The v1 compatibility promise covers only the following versioned contracts and
their deterministic tooling:

| Contract | Supported versions | Migration posture |
| --- | --- | --- |
| `pic-semantics` | `0.1.0` | No prior migration; preserve value-state and decimal-string rules. |
| `pic-crosswalk` | `0.1.0` | No prior migration; additive changes require a new compatible version. |
| `pic-fixtures` | `0.1.0` | No prior migration; fixture promotion remains human-controlled. |
| `pic-parameters` | `0.1.0`, `0.2.0` | `0.1.0` remains supported; `0.2.0` adds `holidayExclusions`. |
| `pic-traces` | `0.1.0`, `0.2.0` | `0.1.0` remains supported; `0.2.0` requires input `valueState` and adds optional `valueOrigin`. |
| `pic-foio-compatibility` | `0.1.0` | Optional profile; it does not make FOI-O runtime-authoritative. |
| `pic-process-profile` | `0.1.0` | Candidate platform-neutral profile; no earlier version migration exists. |

The aggregate programme release is `v1.0.0-rc.1`; it does not collapse the
independent PIC package versions.

## Explicit exclusions

The freeze does not promise compatibility for converters, engine adapters,
Camunda projections, demos, studies, staged external snapshots, candidate
fixtures, papers, or platform-specific process mappings. Those surfaces remain
adapter, experimental, study, or internal evidence as specified by
`docs/V1_SCOPE.md`.

No new contract, jurisdiction profile, expression language, JSON-LD context,
runtime AI decision, or uncertified fixture enters the v1 surface during the
release-candidate freeze.

## Release-candidate change rule

After the freeze base, only release evidence, documentation corrections,
generated manifests, test hardening, and fixes required by a failing gate may
change. Any normative contract change requires a new freeze base, migration
entry, compatibility evidence, and renewed human review.
