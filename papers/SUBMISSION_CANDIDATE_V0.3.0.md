# Paper Programme Submission Candidate v0.3.0

**Prepared:** 2026-07-15  
**Status:** package approved; not submitted  
**Package owner:** Dylan A Mordaunt  
**Submission rule:** no arXiv, journal, or preprint action occurs until Dylan authorizes that specific action.

**Package approval:** Dylan approved package version `v0.3.0` on 2026-07-15.

**Submission sequence:** Dylan will not submit any paper in this package until
the FOI-O v2 update has been submitted to arXiv.

PDF artifacts and hashes: [`release/v0.3.0/MANIFEST.json`](release/v0.3.0/MANIFEST.json).

This is the next version of the paper package. It advances preparation without
claiming that the FOI-O release-evidence bundle, RaC Zenodo mirror, or any
upstream adoption proposal has been accepted.

## Package contents

| Paper | Manuscript | Submission packet | Current evidence boundary |
|---|---|---|---|
| PIC coupling | [`coupling/paper.md`](coupling/paper.md) | [`coupling/ARXIV_SUBMISSION.md`](coupling/ARXIV_SUBMISSION.md) | PIC coupling, NZ OIA clock, and the bounded SNAP comparison; not universal interoperability |
| SNAP divergence | [`../studies/snap-divergence/paper/paper.md`](../studies/snap-divergence/paper/paper.md) | [`../studies/snap-divergence/paper/ARXIV_SUBMISSION.md`](../studies/snap-divergence/paper/ARXIV_SUBMISSION.md) | 50 approved agreements and 15 held divergences; held cases remain source-triangulation outcomes, not blanket bug findings |
| NZ reconciliation | [`../studies/nz-reconciliation/paper/paper.md`](../studies/nz-reconciliation/paper/paper.md) | [`../studies/nz-reconciliation/paper/ARXIV_SUBMISSION.md`](../studies/nz-reconciliation/paper/ARXIV_SUBMISSION.md) | 10 agreements and 7 engine gaps across the 17-case inventory; no claim of legal correctness |

## Evidence baseline

- FOI-O software release: `v0.8.1`, commit
  `d24ae6f9f2d9488052969f633d91eff4a9a47f58`; Zenodo identifiers are recorded
  in the citation ledger, but the release-evidence bundle in
  `edithatogo/foi-o#27` is still pending.
- RaC Conformance software release: `v0.2.0`, commit
  `35fdebdd6ca3ad0a254ca0b3ec5b7466b7db3fe5`; its Zenodo deposit remains
  pending and must not be cited as published until the DOI resolves.
- SNAP approved comparison set: 50 cases; held queue: 15 cases.
- NZ reconciliation inventory: 17 cases; 10 agreements; 7 engine gaps.
- Project 14 governance was human-approved on 2026-07-15.
- External adoption remains maintainer-controlled and is not a paper acceptance
  criterion.

## Candidate preflight

- [x] Shared author metadata, ORCID, affiliations, and no-email policy are present.
- [x] Three manuscripts and three submission packets are present.
- [x] Current numerical claims are linked to committed result artifacts.
- [x] Limitations distinguish agreement from legal validity and divergence from defect.
- [x] FOI-O and Zenodo publication boundaries are explicit.
- [x] Repository `make check` passes.
- [x] Candidate A4 PDFs generated and hashed under `papers/release/v0.3.0/`.
- [ ] Produce venue-specific PDFs and run final PDF/link/word-count checks.
- [ ] Dylan confirms authorship, affiliations, declarations, and target venue for each paper.
- [ ] Dylan authorizes each submission or records a continued deferral.

## Decisions for release

1. **Package version:** **approved** — `Paper Programme Submission Candidate
   v0.3.0` is the working submission package.
2. **Evidence posture:** choose whether to submit with the current explicit
   FOI-O evidence limitation or wait for #27 before making any FOI-O release or
   compatibility claims. The package supports the former only with the boundary
   text retained.
3. **Venue and action:** identify the target venue and authorize PDF generation
   and submission separately for the coupling, SNAP, and NZ papers, after the
   FOI-O v2 arXiv submission prerequisite is satisfied.

Approval of this candidate package is not submission authorization.
