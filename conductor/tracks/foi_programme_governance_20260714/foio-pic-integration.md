# FOI-O and PIC integration recommendations

## Recommended boundary

FOI-O owns the operational model, empirical extraction contract, ontology,
codebook, jurisdiction profiles, and release. RaC Conformance owns the optional
PIC interchange schemas, validators, cross-engine conformance evidence, and
publication-facing compatibility record. Neither repository is a runtime
dependency of the other.

## Release handshake

Use one content-addressed manifest to identify the complete evidence chain:

1. FOI-O release tag, commit, capabilities, schemas, ontology, and codebook.
2. PIC package versions and the compatibility result for each package.
3. Jurisdiction profile, calendar, applicable time, and observation time.
4. `edithatogo/legislation` source-pack revision and digest.
5. `fyi-archive` raw manifest plus Hugging Face dataset repository, immutable
   revision, configuration, split, and digest for derived records.
6. `nlp-policy-nz` pipeline and model versions for machine-derived candidates.
7. Evidence assertion, independent oracle, reviewer, and promotion state.

The manifest should validate offline and should never use a mutable branch name
or `latest` dataset revision as release evidence.

## Governance mapping

PIC `valueState` describes the state of a value. It must not absorb FOI-O's
separate epistemic, review, extraction-method, maturity, or certification axes.
An adapter should preserve each axis explicitly and reject lossy mappings.

## Jurisdiction and time safety

Every exported parameter, fixture, and trace bundle should inherit the same
jurisdiction and bitemporal envelope as its FOI-O source pack. Negative tests
should reject:

- New Zealand evidence used in an Australian profile without an explicit
  comparative mapping;
- Commonwealth rules applied to a state or territory profile;
- legislation, calendar, or ontology versions outside their effective period;
- source, archive, Hugging Face, or release digests that do not match; and
- candidate fixtures presented as independently verified gold fixtures.

## Candidate generation and promotion

FOI-O may export PIC-compatible candidate crosswalks, fixtures, parameters, and
traces. Generation should be deterministic from a pinned release bundle.
Promotion remains a RaC human-review action requiring independent source/oracle
evidence; schema validity alone is insufficient.

## Continuous integration

Each repository should test against a pinned, published artifact from the other
repository. The gates should produce a compatibility matrix and a signed or
content-addressed evidence bundle suitable for the deferred papers refresh.
Checkout-relative integration paths may be used for development but cannot be
the only release proof.

## Analyst review checklist

Before treating a compatibility result as evidence, the analyst should record:

- the exact FOI-O and PIC revisions, artifact paths, and content digests;
- the jurisdiction, legislative period, calendar, applicable time, and
  observation time used by the comparison;
- the source assertion and independent oracle for each candidate mapping or
  fixture, including reviewer and promotion state;
- the validator version and command, plus the complete compatibility result; and
- any missing published artifact as `blocked`, with the owner and next evidence
  required.

`schema-valid`, `locally-tested`, `human-approved`, `published-artifact-tested`,
and `promoted` are distinct analyst outcomes. Do not shorten them to "verified"
or "complete" in a report.
