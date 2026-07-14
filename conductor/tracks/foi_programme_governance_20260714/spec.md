# Freedom of Information programme governance

## Objective

Use GitHub Project 14, Rare Insights Freedom of Information, as the focused
cross-repository programme board while preserving each repository's dedicated
Conductor roadmap as its implementation source of truth.

## In-scope repositories

- `edithatogo/foi-o`
- `edithatogo/fyi-cli`
- `edithatogo/fyi-archive`
- `edithatogo/nlp-policy-nz`
- `edithatogo/rac-conformance`
- `edithatogo/legislation`, limited to FOI legislation source work
- `edithatogo/alaveteli`, limited to upstream workflow/state intelligence

## Rules

- Mirror only FOI-relevant issues and pull requests into Project 14.
- Do not mirror every issue from broad repositories such as `nlp-policy-nz`,
  `legislation`, `rac-conformance`, or the Alaveteli fork.
- Represent Alaveteli as a read-only intelligence/reference dependency unless
  a separately authorized upstream contribution exists.
- Keep local Conductor plans authoritative and Project fields synchronized.
- Track jurisdiction, repository role, dependency, evidence status, human gate,
  and delivery status for cross-repository items.
- Do not use Project 4 or Project 19 as substitutes for this FOI-focused board.
- Treat the FOI-O to PIC relationship as an optional, versioned
  interoperability profile. FOI-O remains authoritative for its runtime,
  schemas, ontology, codebook, and jurisdiction profiles.
- Do not collapse FOI-O epistemic status, human-review status, extraction
  method, or certification status into PIC `valueState`; preserve those axes
  as separate provenance assertions.
- Resolve archive provenance through immutable `fyi-archive` source records and
  explicit Hugging Face dataset repository, revision, split, and content digest.

## FOI-O to PIC compatibility profile

The paired repositories should define a machine-readable release handshake
which pins, without introducing a runtime dependency:

- the FOI-O release tag, commit, schema versions, ontology version, codebook
  version, capability manifest, and migration behavior;
- the PIC package names and versions used by exported crosswalks, parameters,
  fixtures, and traces;
- the jurisdiction profile and calendar version, plus the applicable-time and
  observation-time boundaries;
- the `edithatogo/legislation` source-pack revision and content digest;
- the `fyi-archive` raw manifest and Hugging Face dataset repository, immutable
  revision, configuration, split, and content digest;
- the `nlp-policy-nz` extraction pipeline/model version when a candidate was
  machine-derived; and
- evidence-assertion identifiers, independent-oracle status, curator/reviewer,
  and promotion state for candidate fixtures and mappings.

The profile should be content-addressed, validate offline, and support a
compatibility matrix showing which FOI-O releases have passed which PIC contract
versions. Australian tests must prove that artifacts cannot silently cross a
jurisdiction, legislative version, or calendar boundary.

## Acceptance criteria

- Project 14 documentation names every in-scope repository and its boundary.
- The current FOI-O, archive, NLP, legislation, and RaC issues appear on Project 14.
- Dedicated repository Projects retain their existing items and status.
- A repeatable sync contract documents inclusion filters and prevents unrelated
  open-policy, NLP, legislation, or rules-as-code work from leaking onto the board.
- Project status never implies legal validation, publication, or upstream acceptance.
- A versioned FOI-O to PIC compatibility-profile schema, valid and invalid
  examples, validator tests, and compatibility matrix are planned before the
  next release-evidence bundle is consumed by the papers track.
- Generated fixture and trace candidates retain source/evidence links and remain
  candidates until independently reviewed; FOI-O exports never become golden
  PIC fixtures merely by passing schema validation.
- Release evidence identifies Hugging Face as the derived dataset destination
  owned by `fyi-archive`, while preserving immutable raw archive provenance.
