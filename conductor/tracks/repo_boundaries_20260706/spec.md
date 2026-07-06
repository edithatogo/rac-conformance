# Repo Relevance Boundary Catalog

## Overview

The completed roadmap now points at several adjacent `edithatogo` repositories. This track creates a maintained boundary catalog so future agents only touch repositories that are actually relevant to the rules/process roadmap.

## Functional Requirements

1. Maintain `conductor/edithatogo-repo-boundaries.md` as the source of truth for repo relevance.
2. Classify repositories into:
   - currently relevant;
   - potentially relevant with a named consumer;
   - not relevant by default;
   - external non-`edithatogo` targets.
3. For every currently relevant repo, name the exact roadmap boundary and the type of work allowed.
4. For every potentially relevant repo, define the entry condition for creating a track.
5. Add a checkable policy that future tracks cannot pull in a repo without a consumer, exact path, and acceptance criteria.

## Non-Functional Requirements

- Keep this as governance documentation, not a code dependency.
- Do not claim a repository is permanently irrelevant; instead state that it is out of scope unless a future product decision names it.
- Use live repo metadata where practical, but treat descriptions as hints rather than authority.

## Acceptance Criteria

- Boundary catalog exists and covers all `edithatogo` repositories identified during the July 2026 audit.
- `conductor/tracks.md` lists this track ahead of implementation tracks.
- `make check` passes.
- Phase checkpoint records whether any repository needs immediate follow-up.

## Out Of Scope

- Editing external repositories.
- Opening GitHub issues or PRs.
- Reclassifying non-`edithatogo` upstream projects beyond noting their relevance.
