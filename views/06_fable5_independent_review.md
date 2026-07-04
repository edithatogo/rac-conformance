# Fable 5 independent review of RaCX (2026-07-04)

Reviewer: Claude Fable 5 (Cursor). Full pack read: views, conversation outputs, original Google AI Mode transcript, and the conceived `project_repo_racx/` down to schemas, examples, validator, evaluator, tests, and CI.

## 1. Executive summary

**Verdict: the direction is strategically promising; the packaging is over-scoped, under-specified where it matters most, and built without a demonstrated consumer. The valuable core is smaller than RaCX claims, and it is not the JSON-LD lifecycle package. It is the conformance layer: shared test fixtures, a trace contract, temporal parameter interchange, and a concept-ID crosswalk, proven by differential testing between real engines.**

- **Keep:** stable concept IDs, temporal parameter model, engine-neutral test fixtures, trace contract, source references, the missingness taxonomy (the single best technical idea in the pack), sidecar-first adoption, "no runtime AI for decisions".
- **Drop from v0.1:** the "superset" name and claim; mapping tables to 15+ standards; the evidence-confidence model as mandatory; process exchange; the invented `racx-expression-v0.1` language.
- **Reframe:** RaCX is not an exchange format that comes with tests. It is a **conformance and comparison harness that comes with a format**.

Structural observation: ChatGPT's own red-team (`views/02`) identifies nearly every major risk — superset sprawl, hidden IR, standards overload, adoption friction, governance vacuum — and the conceived repo does not act on most of them. Diagnosis without treatment.

## 2. Where I agree

1. The gap is real: parameters, APIs, datasets move between RaC systems; executable logic, semantics, tests, and traces do not. Nobody owns the comparison problem, and it grows as AI generates policy models faster (Axiom's exact situation).
2. Sidecar-first, no-rewrite adoption is right; the seven-level ladder is correctly ordered.
3. No runtime LLM decisions — non-negotiable. The "Rule Maker pattern" division of labor is correct.
4. ChatGPT's correction of the Google AI Mode transcript's "95–100% translation, zero technical debt" claims was sound.
5. The missingness taxonomy (zero / false / unknown / not-provided / not-applicable / unverified / stale / conflicting) is genuinely good and uncovered by existing standards. Headline feature, not a footnote.
6. Rules and process are more related than typical RaC tooling admits — with the caveats in section 3.
7. Federated crosswalk, not replacement ontology — right correction, not propagated into the artifacts.

## 3. Where I disagree

### 3.1 The canonical JSON-LD lifecycle package should not be the v0.1 deliverable

A canonical model is a commitment you earn, not start with. Standards that survive are extracted from working exchanges (Markdown, OpenAPI, HDF5), not designed ahead of them. v0.1 should ship four **independent artifact specs** sharing only an ID convention — parameters, fixtures, traces, concept crosswalk — each adoptable alone, each with a working converter. JSON-LD `@context` should be an optional overlay ("plain-JSON usable, JSON-LD compatible").

### 3.2 Rules/process coupling: right thesis, wrong sequencing

| Concern | Couple to rules? | How |
|---|---|---|
| Legal entitlement logic | Core | Pure, channel-free decision services with source refs and parameters |
| Evidence & verification | **Yes — tightest legitimate coupling** | Verification state feeds missingness semantics of variables; statutory evidence rules are law, not ops |
| Administrative process | No — interface only | Process steps *reference* decision IDs; decisions never know their invoking channel |
| Human discretion / case mgmt | Must stay separate | Typed *discretion points* (who decides, required reasons, review path) — never expressions |
| Notices & review rights | Couple to decision *outputs* | Reason codes and appealable-decision flags are decision outputs, not workflow properties |
| Operational/service design | Do not standardize | Channel-specific |
| Fiscal/distributional evaluation | Couples to rules + parameters | Needs population/period/weight semantics, not process |
| Administrative burden evaluation | Best argument for process metadata | ~80% achievable from evidence requirements + step counts + time limits without a workflow language |

Organizing principle: **couple through identifiers, never through embedding, because these artifacts change at different cadences and are owned by different institutions.** Entitlement logic changes with legislation; process changes with agency operations; service design changes with product sprints. `normativeStatus` is a good start; extend it with change-cadence and ownership annotations.

### 3.3 "AI enables rapid redesign to remove technical debt" is true for code, approximately false for standards

A format's value *is* its stability and installed base. If AI makes redesign cheap for you, it makes it cheap for everyone — including the option of not standardizing and letting agents translate engine-to-engine on demand. The part that survives: **agents translate cheaply but not verifiably.** The durable AI-era value is what makes any translation checkable — fixtures, traces, differential conformance. The harness is the product.

### 3.4 The superset framing is wrong, and the pack knows it

See section 8.

## 4. Biggest risks (ranked)

1. **No demonstrated consumer.** Nothing cites a maintainer asking for any of this. Entirely supply-side. This kills it regardless of spec quality.
2. **The vectorized-trace problem is load-bearing and unconfronted.** OpenFisca/PolicyEngine compute arrays over populations; there is no per-case decision path in the sense the trace schema assumes. Deriving case-shaped traces from vectorized execution (per-case re-execution, sampled tracing, computation-tree projection) is real engineering the pack never mentions.
3. **Perceived Axiom capture.** "Axiom could become the authoring and migration workbench for RaCX" reads as ecosystem-standard strategy by an Axiom-adjacent author. Governance neutrality must be designed in from day one.
4. **Sidecar staleness.** Hand-maintained sidecars go stale on the first merged PR. The sidecar must be *generated* from native code in CI: the exporter is the deliverable, the sidecar the artifact.
5. **Correlated AI errors.** If the same model generates mapping, adapter, and tests, the tests won't catch the mapping's misunderstanding. The conformance oracle must be independent: human-curated golden cases from legislation/worked examples, or an unrelated implementation.
6. **Echo-chamber provenance.** The red-team of the assistant was written by the assistant; the pack is one model's dialogue with one user, with a visible agreement gradient. Treat every point where the assistant reversed itself under user pressure as unvalidated.
7. **Fixtures mistaken for law.** Golden cases encode contestable interpretations; each needs a versioned interpreter-of-record and an explicit non-authoritative disclaimer.

## 5. Recommended architecture

A **conformance-first artifact suite** (sidecar-only + conformance-test-only hybrid, deferred canonical package):

```text
Layer 0  Concept ID scheme + crosswalk tables (plain JSON/CSV)
Layer 1  Artifact specs (independent, each adoptable alone):
         parameters / fixtures / traces / source refs
Layer 2  Tools (the actual product):
         exporters (generate sidecars from native code)
         runners (execute fixtures against native engines)
         differ  (differential conformance report across >=2 engines)
Layer 3  (Deferred, evidence-gated)
         package manifest + optional JSON-LD contexts
         expression profile — adopt an existing small language
         (JSON Logic subset or FEEL subset), do not invent one
         RaCX-Process / RaCX-Evidence as separately versioned experiments
```

Against the alternatives: a separate IR is the same commitment with worse branding; no existing standard covers microsimulation + temporal parameters + missingness (DMN/BPMN enterprise-biased XML, LegalRuleML unadopted); Axiom-native canonical maximizes capture risk although Axiom-first *tooling* is right; DMN/BPMN-first and JSON Logic/XState-first each smuggle one deployment context's assumptions into the policy layer. The JSON-LD package is the best of the options as posed — the disagreement is sequencing, not destination.

**The expression language is the trap**: highest cost, lowest early value, where every prior effort stalled. Defer or adopt an existing evaluable subset.

## 6. MVP design

**A differential conformance demonstration on one real policy between two real engines.** Crosswalk table; parameter export + diff; 30–50 human-curated golden fixtures from legislation/worked examples; runners for both engines; published divergence report with root causes.

Success criterion: **the report finds at least one real, previously unknown discrepancy, and a maintainer accepts a resulting issue or PR.**

## 7. Adoption path

- Add Level 0: crosswalk tables (pure data, no code in host repos).
- Align with what exists: OpenFisca already has YAML tests and a trace capability; PolicyEngine has computation trees and structured parameter metadata. Design fixture/trace specs as *normalizations of those*.
- Exporters run from this project's CI against upstream repos first; propose in-repo adoption only after proven stable.
- **Axiom is the wedge, and validation is Axiom's real problem**: an AI system generating policy models needs to verify them against reference implementations. Build the harness as Axiom's QA layer, then generalize.
- Scope Level-4 traces to scalar/household calculations until the vectorized story exists.

## 8. Ontology/superset strategy

The superset claim is wrong as stated. Upper ontologies and universal crosswalks historically produce impressive mapping tables and near-zero adoption. What is needed: a shared identifier scheme + crosswalks for a small set of object types, maintained lazily where a consumer exists.

- Minimum viable core: `Concept`, `Variable`, `TemporalParameter`, `TestFixture`, `Trace`, `SourceRef` — six types. `Decision`, `EvidenceRequirement`, `ProcessStep`, `CaseAction` are Layer-3 extensions.
- Hard rule: no standard appears in any mapping table without (a) a working, tested converter and (b) a named consumer.
- Public framing: "policy conformance and interchange profiles", not "superset".
- Concept registry: defer global registration; jurisdiction- and package-scoped IDs suffice for years.

## 9. AI usage strategy

Genuinely cheaper with AI: exporter/adapter scaffolding, parameter migration, boundary-case *proposal* (human-approved), crosswalk drafting, sidecar sync, divergence explanation, schema red-teaming.

Debt/false-confidence zones:

1. Semantic mapping (an LLM will map `income` to `income` across systems where they differ — the exact failure this project exists to prevent). Human signature + a fixture that fails if the mapping is wrong.
2. Correlated code/test errors. Oracle independence: fixtures from legislation, agency examples, or an unrelated implementation — never from the model that wrote the adapter.
3. Spec changes move at human-governance speed regardless of how fast AI can draft them: semantic versioning, deprecation windows, change-proposal process.

Strategic line: **in an agentic world, translation is cheap and verification is scarce. This project sells verification.**

## 10. Specific repo/spec edits (ordered)

1. Specify or remove `racx-expression-v0.1` — the most load-bearing undefined symbol in the repo.
2. Make the missingness taxonomy executable (enum + propagation rules through `and`/`if`/comparisons; evaluator currently KeyErrors on absent input).
3. Fix the reference evaluator: no `or`, no arithmetic, digit-string `Decimal` coercion via `str.replace('.','',1).isdigit()` mangles negatives/exponents in a spec that mandates decimal-safe money.
4. Validate the whole package: per-file schema validation driven by the manifest; referential integrity (decision inputs reference declared variables, etc.); negative-test suite of invalid packages. Seven of nine schemas are never loaded by anything.
5. Close the loop in tests: load manifest → run golden cases through declared decisions → compare expected → emit trace validated against trace schema.
6. Give `trace.schema.json` a real `steps` schema; address or scope out batch/vectorized traces.
7. Publish the JSON-LD context or demote JSON-LD to optional.
8. Governance files: CONTRIBUTING, spec versioning policy, change process, decision authority.
9. Descope the example manifest (a 3-variable toy declaring five profiles models the over-scoping being warned against).
10. Hygiene: gitignore caches; constrain `manifest.schema.json` `files` values.
11. Resequence roadmap: crosswalk + parameter diff for a real policy pair first; fixtures + two native runners + divergence report second; maintainer engagement third. Cut DMN/JSON Logic export and workbench prototype from the first 90 days.

## 11. Questions asked of Dylan (and his answers, 2026-07-04)

1. Who is the second party? — **"Nobody yet."**
2. Is the real problem validating Axiom-generated models? — **"No real problem. This was an idea."**
3. Which policy/jurisdiction pair for a pilot? — **"No idea."**
4. Vectorized trace answer? — **"No idea."**
5. Admin-burden partner? — **"No idea — identify options from public data."**
6. Governance home? — **"Start with me, publish on arXiv, hope others adopt."**
7. Talk to L4/Catala? — **"Too much work; trying to leapfrog with bleeding-edge AI."**
8. Interpreter of record for fixtures? — **"No idea. Needs to be open."**

These answers ruled out the standards path and triggered the reassessment in `views/07`.

## 12. Final verdict

Promising direction, wrong packaging. Ship the conformance harness first — crosswalks, temporal parameters, human-curated fixtures, traces, and a differential runner that finds a real divergence between two real engines — and extract the canonical package later from exchanges that demonstrably work. Keep the missingness semantics as the technical crown jewel, treat Axiom's model-validation need as the funded wedge, put governance neutrality in writing before approaching OpenFisca, and hold the expression language and process profiles at the door until Levels 0–4 have at least one external adopter.
