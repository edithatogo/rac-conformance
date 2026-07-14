# PIC FOI-O compatibility profile 0.1.0

This optional manifest binds a released FOI-O ontology/profile family to PIC
contract versions and its legislation, archive, Hugging Face, NLP, jurisdiction,
calendar, and governance evidence. It is an interchange record, not a runtime
dependency and not a legal certification.

Mutable revisions such as `main` and `latest` are forbidden. FOI-O epistemic,
review, extraction, certification, and promotion states remain separate from
PIC value states. Model-derived records cannot be certified or promoted to gold;
gold promotion requires an independent oracle and adjudicated or approved review.

`picArtifacts` wraps one fixture, parameter set, and trace without changing the
underlying PIC contracts. Every wrapper carries the contract version, immutable
artifact coordinate and digest, jurisdiction, applicable and observation times,
and evidence references. The deterministic validator requires those values to
match the release envelope and rejects evidence references not declared by the
governance assertion ledger.

`pic-foio-check` validates a downloaded bundle without network access. The
bundle stores each PIC artifact under `artifacts/<sha256>` and retains its
immutable publication URI in the wrapper. The compatibility matrix must report
an absent FOI-O release as blocked; a synthetic contract example is not release
evidence and cannot produce a `passed` row.

Every generated fixture or crosswalk candidate also carries a promotion record.
Approval requires a reviewer independent of the producer and immutable review
evidence. Pending or rejected records cannot be represented as promoted gold
fixtures, and candidate-kind/requested-promotion mismatches fail validation.
