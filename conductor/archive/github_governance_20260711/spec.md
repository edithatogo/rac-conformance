# GitHub governance and security configuration

## Objective

Make GitHub settings enforce the repository’s tested contribution and security policies.

## Requirements

- Protect `main` against force pushes/deletion and require pull requests, resolved conversations, and current required checks where supported.
- Enable secret scanning, push protection, validity checks, and Dependabot security updates where the repository/account supports them.
- Give Project 19 a useful public description/readme and views for active external review, blockers, papers, and completed work.
- Resolve issue #6 as completed roadmap history or a narrowly scoped monitoring parent; do not leave contradictory status.
- Document any GitHub-plan or repository-visibility limitation that prevents a setting.

## Acceptance

- GitHub API evidence records every applied setting and unsupported setting.
- Governance documentation matches actual settings.
- No protection rule blocks trusted maintenance without an explicit recovery path.
