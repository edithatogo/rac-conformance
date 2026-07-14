Conductor track: `foi_programme_governance_20260714`

Use GitHub Project 14 as the focused FOI programme board across `foi-o`,
`fyi-cli`, `fyi-archive`, `nlp-policy-nz`, `rac-conformance`, FOI-specific
`legislation` work, and Alaveteli workflow/state intelligence.

Keep repository-native Conductor plans authoritative, retain dedicated Project
membership, mirror only FOI-relevant items from multi-purpose repositories, and
add drift checks for missing, stale, or unrelated Project 14 items.

## FOI-O to PIC pairing

Define an optional, versioned compatibility profile. FOI-O remains authoritative
for its runtime, schemas, ontology, codebook, and jurisdiction profiles; PIC is
an interchange and conformance layer and is not a FOI-O runtime dependency.

The release handshake must pin:

- FOI-O release/tag/SHA, capabilities, schemas, ontology, codebook, and migrations;
- PIC package versions and compatibility results;
- jurisdiction profile, calendar, applicable time, and observation time;
- `edithatogo/legislation` source-pack revision and digest;
- immutable `fyi-archive` raw provenance and Hugging Face derived-dataset
  repository/revision/configuration/split/digest;
- `nlp-policy-nz` pipeline/model version for derived candidates; and
- evidence assertions, independent oracle, curator/reviewer, and promotion state.

Preserve FOI-O epistemic, review, extraction, maturity, and certification axes;
do not collapse them into PIC `valueState`. Add offline validation, valid and
negative examples, a compatibility matrix, and cross-jurisdiction/time/digest
leakage tests. Generated mappings, fixtures, parameters, and traces remain
candidates until independently reviewed.

Detailed recommendations:
`conductor/tracks/foi_programme_governance_20260714/foio-pic-integration.md`.
