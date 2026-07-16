# Consumer Inventory

This inventory keeps the profile deliberately small. A field is included only
when an identified consumer needs it or when it is required to verify a stated
PIC invariant.

| Concept | Consumer | Evidence | Required behavior |
| --- | --- | --- | --- |
| Process/state/transition IDs | FOI-O baseline, future health profiles, Camunda adapter | `conductor/tracks/foi_programme_governance_20260714/foio-pic-integration.md`; `camunda_portability_20260714/spec.md` | Stable references; adapters may rename display labels but not IDs. |
| Actors and authority links | FOI-O casework, adverse-incident review, optional adapters | `pic_process_profile_20260714/spec.md`; `adverse_incident_open_disclosure_20260714/spec.md` | Actor kind is explicit; authority is source-linked and never inferred from a label. |
| Timers and deadlines | FOI-O statutory clocks and future health pathways | `external/foi-o/rules/SOURCES.md`; `health_technology_pathways_20260714/spec.md` | A timer identifies its start event and duration; rule/parameter contracts own calendar arithmetic. |
| Observed and derived events | FOI-O and `foi-process` evidence | `external/foi-o/rules/DESIGN.md`; `subrepos/process-mappings/profiles/foi/README.md` | Preserve occurrence and observation times and source references. |
| Human tasks and certified decisions | adverse-incident profile and FOI review workflows | `adverse_incident_open_disclosure_20260714/spec.md`; `pic_process_profile_20260714/spec.md` | Never collapse proposed actions into certified decisions. |
| Deterministic rule invocations | existing PIC fixtures, parameters, and traces | `contracts/pic-fixtures/`; `contracts/pic-parameters/`; `contracts/pic-traces/` | Link by released contract identifiers; invocation is deterministic. |
| Source assertions and effective dates | every source-backed profile | `subrepos/process-mappings/REPOSITORY_BOUNDARY.md`; Track 5 triangulation rules | Fail closed for unreviewed controlling sources or missing effective dates. |
| Evidence references and normalized traces | conformance reports and optional platform adapters | `contracts/pic-foio-compatibility/`; `camunda_portability_20260714/spec.md` | Preserve hashes and state representational loss explicitly. |

The profile intentionally does not include BPMN, DMN, FEEL, a global ontology,
an expression language, or executable clinical/legal judgement. Those are
consumer-specific implementation concerns and have no normative PIC consumer
requirement at this stage.
