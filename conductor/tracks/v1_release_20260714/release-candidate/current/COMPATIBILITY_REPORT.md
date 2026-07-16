# Current v1.0.0-rc.1 Compatibility Report

Candidate source commit: `4206608baa37c4844cb4aee4a629797df9479ff9`.

The candidate uses the frozen PIC contract package versions and the migration
and compatibility rules in `docs/V1_COMPATIBILITY.md`. The current source
archive and `pic-contracts` wheel/sdist were built twice from clean output
directories and matched byte-for-byte.

Automated evidence: local `make check`; hosted Ubuntu/macOS and Python
3.12/3.13 qualification; Contracts, Quality, Dependency Review, workflow
security/lint, and CodeQL; and the valid/invalid example and converter corpora.

This report does not certify FOI-O source authority, health-technology
mappings, independent adoption, human fixture promotion, signing, publication,
or legal/clinical/funding correctness. Those remain release gates.
