# Adoption Closure And External Proof

## Overview

The first roadmap produced evidence and staged submissions. This track turns those staged artifacts into external proof where possible: live issues, PRs, CI links, responses, merge status, or explicit external blockers.

## Functional Requirements

1. Inventory every staged external artifact:
   - `external/foi-o/SUBMISSION.md`
   - `external/policyengine/SUBMISSION.md`
   - `external/policyengine/SUBMISSION_trace.md`
   - `external/policyengine/SUBMISSION_missingness.md`
   - `external/openfisca/SUBMISSION.md`
   - `external/openfisca/SUBMISSION_missingness.md`
   - `external/alaveteli/SUBMISSION.md`
   - `external/dbn/EMAIL.md` and `external/dbn/LOG.md`
2. Create `external/ADOPTION_STATUS.md` with one row per external target.
3. For each target, record:
   - artifact path;
   - intended upstream location;
   - current state: staged, sent, opened, submitted, under review, merged, declined, blocked;
   - CI/Actions status where applicable;
   - exact URL for issue/PR/email response if available;
   - next required actor.
4. Prepare patch branches or PR-ready bundles for targets where the current agent has access.
5. Monitor GitHub Actions/CI after any branch/PR creation and apply review/CI fixes within the authorized repository.
6. Record external gates honestly. If merge authority or maintainer response is missing, mark it blocked with the exact requirement instead of calling it complete.

## Non-Functional Requirements

- External repo work must respect each target repository's own contribution style.
- Do not force PIC branding into upstream contributions; lead with the maintainer's problem.
- Do not claim merge, publication, or acceptance without a URL or repo-local log evidence.
- Use one commit per task in this repository; external repositories get their own commits/branches only when explicitly touched.

## Acceptance Criteria

- `external/ADOPTION_STATUS.md` exists and is current.
- All staged submissions are either live externally, explicitly superseded, or marked with a concrete blocker.
- Any created PRs have passing required GitHub Actions, or a failing-check diagnosis with fixes applied where permitted.
- Merged PRs are recorded with URLs. Unmerged PRs list the remaining reviewer/maintainer action.
- `make check` passes in this repo before the phase is checkpointed.

## Out Of Scope

- Rewriting the underlying PIC contracts.
- Creating new demos.
- Merging PRs in repositories where the agent lacks authority.
- Sending emails or posting issues without Dylan's approval when the target is marked `[HUMAN]`.
