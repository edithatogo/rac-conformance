# Spec: Community, process-side contributions, and papers

## Purpose

Convert the technical tracks into adoption and standing: engage the one community with documented demand for an open rules standard, contribute the process-side state model upstream, and publish the coupling paper. Everything here is gated on evidence existing first — this track mostly *consumes* outputs from Tracks 1–5.

## W-A: Digital Benefits Network Rules-as-Code CoP

- Gate: at least one of {Track 2 merged into foi-o, Track 5 report drafted} exists.
- Deliverable: `external/dbn/EMAIL.md` — introduction email to rulesascode@georgetown.edu: who Dylan is (foi-o, PolicyEngine/Axiom), the finding (divergence report and/or the OIA coupling demo), one specific offer (present at a roundtable; share fixture format), one specific ask (which programs/states the CoP most wants compared next). Their published context to reference: cross-sector insights report's "open standard + shared code library" finding; the AI-Powered Rules as Code report's verification gap.
- `[HUMAN]` sends; agents draft and keep a contact log (`external/dbn/LOG.md`).

## W-B: Alaveteli / mySociety upstream

- Gate: Track 2 phase 3 complete (the state model is proven in foi-o).
- foi-o already normalizes Alaveteli/FYI request states. Deliverable: `external/alaveteli/SUBMISSION.md` proposing (as an issue/discussion, not a Ruby PR): a documented, versioned request-state taxonomy with statutory-clock metadata hooks, informed by foi-o's normalization experience — value to them: consistent analytics across Alaveteli deployments, machine-readable deadline tracking. Include the mapping table (Alaveteli states ↔ foi-o normalized states) as evidence.
- Data/spec contribution only; no Ruby code unless trivially small.

## W-C: Docassemble and CiviForm (exploratory, lowest priority)

- Deliverable: one-page opportunity assessments each (`external/docassemble/ASSESSMENT.md`, `external/civiform/ASSESSMENT.md`): where an external declarative rule invocation with traces would fit their architecture; what the smallest credible demo would be (e.g. a Docassemble interview invoking a PIC-fixture-tested rule function). No submission until a demo exists; the assessment decides whether to create a follow-up track.

## W-D: Companion paper — "coupling statutory rules and administrative process"

- Gate: Tracks 2 and (5 or 3) complete enough to cite.
- Deliverable: `papers/coupling/` draft. Thesis: rules and process artifacts can share fixture/trace/semantics contracts across a process-heavy domain (OIA) and a rules-heavy domain (SNAP/tax-benefit), with coupling through identifiers and typed invocation; discretion modeled as non-computable points. Evidence: foi-o OIA module (differential agreement result), fixture-converter corpus stats, divergence-study findings. Positioning: companion to the foi-o preprint; cites Policy2Code/DBN verification gap; related work covers L4/Catala/LegalRuleML honestly (what they attempted, what adoption showed).
- Venue: arXiv first; then IJM or JURIX/ICAIL short paper — `[HUMAN]` decision.

## Acceptance criteria

1. Every outreach artifact is gated on its evidence existing (no cold pitches of unproven formats).
2. DBN email sent (`[HUMAN]`) and logged; any response actioned into follow-ups.
3. Alaveteli submission drafted with the real mapping table.
4. Paper draft complete with all claims traceable to repo artifacts.

## Out of scope

Standards-body formation; talks/conferences beyond the DBN roundtable offer; any promotion of PIC as "a standard" (it is "formats used by these working tools" until further notice).
