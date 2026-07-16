# FOI Compatibility Profile

Planned home for mapping FOI-O semantic exports and foi-process execution
evidence into released PIC process-profile contracts.

- FOI-O remains the semantic and jurisdiction-profile authority.
- foi-process remains the deterministic event/replay/OCEL implementation and
  evidence source.
- This profile records compatibility, provenance, and representational loss; it
  does not reinterpret FOI law or become a runtime dependency of either repo.

No FOI mapping is implemented yet.

The current integration boundary is recorded in
`../../schemas/contract-consumption.json` (relative to this profile). It
does not promote any FOI-O or foi-process artifact to a legal or normative
authority: FOI-O supplies semantic input, while foi-process supplies execution
and evidence input. Any representational loss must be recorded before a
profile can be proposed.
