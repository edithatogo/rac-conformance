# Independent Validation Policy

An implementation qualifies only when its organisation, repository, codebase,
fixture curation, oracle, and execution are independent of the maintainer's
release repository. A maintainer-owned fork, agent-generated fixture, paper,
issue, screenshot, or silence is not adoption evidence.

## Outcomes

- `qualifying`: complete, reproducible, independently generated results.
- `partial`: useful execution evidence with a documented missing criterion.
- `conflicting`: results disagree with the expected-result policy and require
  defect classification.
- `withdrawn`, `declined`, and `unresponsive`: tracked but never counted.

Evidence must identify the implementation revision, environment, corpus digest,
oracle method, result digest, and maintainer acknowledgement. The local
verifier checks structure and provenance; it does not certify the external
organisation or silently convert a partial result into adoption.
