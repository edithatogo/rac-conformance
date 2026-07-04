# Product Guidelines

## Prose and documentation style

- Plain, precise, technical English. No marketing language. No claims of "perfect translation", "zero technical debt", "legally authoritative", or "superset".
- Every capability claim must be paired with its scope limit (e.g. "traces for scalar/household calculations; vectorized derivation is out of scope for v0.1").
- Specs use RFC 2119 keywords (MUST/SHOULD/MAY) sparingly and only in normative sections. Every spec has a Status line: `Draft | Consumed-by: <list>`.
- Findings documents (divergence reports, studies) lead with the result, then method, then caveats. Citations to primary sources (statute sections, agency manuals, repo permalinks) are mandatory.

## Naming

- The project's public naming avoids "RaCX" and "superset". Working name for the contracts: **Policy Interchange Contracts (PIC)** — plain, descriptive, unclaimed. Individual contracts: `pic-crosswalk`, `pic-parameters`, `pic-fixtures`, `pic-traces`, `pic-semantics`.
- IDs are jurisdiction- and package-scoped: `nz-oia/…`, `us-snap/…`. No global registry.

## Non-negotiable content rules

1. **No runtime AI decisions.** AI drafts artifacts; deterministic code validates and executes; humans certify. This sentence appears in every externally facing README.
2. **Oracle independence.** Golden fixtures are human-curated from legislation, agency worked examples, or an unrelated implementation. AI may *propose* boundary cases; a human approves each one; provenance is recorded per fixture (`curator`, `source`, `method: human|ai-proposed-human-approved`).
3. **Fixtures are interpretations, not law.** Every fixture file carries `interpreterOfRecord` and a disclaimer field.
4. **No mapping without a consumer.** No crosswalk or export target is added without a working converter and a named user.
5. **Upstream etiquette.** Contributions to other repos solve that repo's problem in that repo's idiom; the contracts are referenced in a "format" footnote, never as the headline. Never open more than one unresolved proposal per upstream repo at a time.

## Versioning and change control

- Contracts use semantic versioning independently of each other (`pic-fixtures/0.2.0` may ship while `pic-traces` stays at 0.1.x).
- Breaking changes require: a CHANGELOG entry, a migration note, and confirmation that all known consumers have been notified (tracked in `contracts/CONSUMERS.md`).
- Spec changes move at human-review speed regardless of how fast an agent can draft them.

## Licensing

- Code and schemas: MIT (matches foi-o). Documents: CC-BY-4.0. Third-party data (PRD, FYI archive) retains its original terms and is never committed here.
