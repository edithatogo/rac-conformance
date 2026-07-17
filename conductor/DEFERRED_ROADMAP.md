# Deferred Roadmap

Status: active deferral decision, 2026-07-17.

The programme is temporarily focused on the core model and one demonstrator.
Deferred work remains tracked, but must not displace
`core_model_demonstrator_20260717`.

| Deferred area | Tracks/issues | Re-entry condition |
| --- | --- | --- |
| Remaining health-technology pathway breadth, certification, and publication | [#42](https://github.com/edithatogo/rac-conformance/issues/42) | Core demonstrator is certified and a new named consumer or second-domain evidence question is approved. |
| Remaining Camunda controlled-runtime, trace, migration, reconciliation, and packaging evidence | [#43](https://github.com/edithatogo/rac-conformance/issues/43) | A certified demonstrator exists and the adapter has a named portability question, pinned runtime, and maintainer capacity. |
| Process-mappings canonical cutover | [#50](https://github.com/edithatogo/rac-conformance/issues/50) | Human approval of version policy and canonical source-of-truth cutover; parent consumers are ready to migrate in one transaction. |
| Independent external validation/adoption | [#23](https://github.com/edithatogo/rac-conformance/issues/23), [#45](https://github.com/edithatogo/rac-conformance/issues/45) | A named external maintainer or organisation accepts a bounded evaluation route and supplies independently controlled evidence. |
| Engineering GA qualification | [#44](https://github.com/edithatogo/rac-conformance/issues/44), [#46](https://github.com/edithatogo/rac-conformance/issues/46) | Core readiness packet is complete, then hosted attestations, signing, live rollback, residual-risk certification, and all applicable external gates are available. |
| Papers and publication | [#15](https://github.com/edithatogo/rac-conformance/issues/15), [#16](https://github.com/edithatogo/rac-conformance/issues/16), [#24](https://github.com/edithatogo/rac-conformance/issues/24), [#31](https://github.com/edithatogo/rac-conformance/issues/31) | Core claims are frozen and the dependent FOI-O release/paper gate is resolved; submission authorization is separately granted. |
| Zenodo and citation deposition | [#33](https://github.com/edithatogo/rac-conformance/issues/33) | Exact release artifact is approved and authenticated human deposition is authorized. |
| FOI programme governance and upstream release | [#30](https://github.com/edithatogo/rac-conformance/issues/30) | Upstream FOI-O evidence and Project 14 verification are available for the declared release boundary. |

## Deferral rules

- Deferred work may receive documentation-only maintenance for correctness or
  safety, but no new implementation breadth should be started under the active
  core track.
- A deferred item cannot be marked complete from local preparation alone.
- Re-entry requires a new Conductor checkpoint naming the consumer, scope,
  dependencies, human gates, and expected evidence.
- Publication, adoption, legal/source certification, and repository cutover
  remain separate human or external gates.
