# Rollback and Vulnerability Rehearsal

This is the v1 tabletop procedure. Historical evidence is never deleted.

1. Freeze the affected release commit and mark the artifact `withdrawn` in the
   release ledger.
2. Publish a deprecation/upgrade notice pointing to the last known-good
   immutable artifact and checksum.
3. Restore `release/v1/gates.json`, SBOM, and compatibility metadata from the
   reviewed commit or repository archive.
4. Apply a regression-first patch, rerun `make check`, and compare checksums.
5. Require human approval before signing or republishing any replacement.
6. Verify the public artifact from a clean environment and record the result.

No public release has been published in this candidate state, so a live yank
has not been performed. The rehearsal remains a required human/hosted evidence
item for v1.0.
