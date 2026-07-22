# OpenFisca response and AI-policy drafts

Status: staged only. Each external comment requires separate final human
approval. Do not publish before the timing and conduct gates below are met.

## RFC #1372 policy contribution

Earliest publication: seven full days after the corrective repository change
is merged. Recheck that the RFC remains open, that the referenced policy files
are still absent from `master`, and that no personal escalation has occurred.

> Hi, I've read this RFC after reviewing what went wrong with my recent OpenFisca submissions. I agree with its central principle: anyone submitting AI-assisted work must remain responsible for it, understand it, and verify it.
>
> I think the policy would be stronger if it addressed publication and scope controls as well as authorship. In #1382, fork-maintenance changes entered the feature branch through a merge from my fork's default branch. I understood and tested the intended feature, but I didn't adequately verify the complete final diff against the upstream base. That created avoidable review and security-assessment work.
>
> I'd suggest requiring:
>
> - verification of the base and head repositories, commit history, merge commits, and final changed-file list;
> - explicit human approval for each upstream action, including opening or updating a PR, commenting, merging branches, and tagging maintainers;
> - separate submissions and specialist review for workflow, release, packaging, permission, and credential-related changes;
> - a factual disclosure of tools used, tasks delegated, human review performed, tests reproduced, and any external actions performed by an agent;
> - limits or prior approval for automated submission volume and maintainer outreach;
> - code-provenance, licence, confidential-prompt, and secret-handling requirements.
>
> The current categories overlap and depend partly on subjective judgments about who was "driving." A factual disclosure would be easier to apply consistently than labels such as "AI-assisted" or "AI-vibecoded."
>
> I'd also recommend proportionate enforcement. For a good-faith first failure, maintainers could request clarification, disclosure, a smaller scope, or a clean branch. Immediate closure would remain appropriate when someone can't explain the work, refuses to correct it, or repeatedly disregards the policy.
>
> Finally, contributor and reviewer conduct should be addressed together. Reviews should focus on observable work and conduct, ask for clarification before inferring identity or motive, and express criticism specifically and courteously. Those standards needn't dilute strict technical review.
>
> Once adopted, the policy should have an effective date and be linked from `CONTRIBUTING.md` and the PR template. The disclosure and reviewer files referenced by this RFC aren't currently present on `master`.
>
> I'm not asking for #1382 to be reopened. I'm offering it as a concrete example of why authorship expectations and technical publication controls need to sit alongside each other.

## Issue #1380 closing response

Earliest publication: 72 hours after the RFC comment. Before approval, replace
`[RFC COMMENT LINK]` with its permanent URL. Do not publish if OpenFisca has
asked for no further contact, the issue is locked, or the RFC discussion has
escalated personally.

> Thanks for the direct response. I've recorded OpenFisca's decision as declined. It won't be treated as adoption, conformance evidence, or an unresponsive candidate, and I won't make further participation requests.
>
> You're right that my follow-up changed the nature of this issue. It began as a concrete missingness question, but I later introduced a broader validation request without first establishing whether OpenFisca wanted to participate. The deadline made a voluntary request sound compulsory. That was a mistake.
>
> For context, to my knowledge I've been the only person undertaking recent visible development work on OpenFisca Aotearoa since activity in the upstream repositories slowed in 2025. I've largely been working in isolation, without an active community in which to test these ideas or establish a contribution pathway. That helps explain my approach, but it doesn't excuse the failures in outreach or final publication review.
>
> I'm also an unfunded researcher. This work isn't commercially funded or commissioned. I've used AI and automation because they've made research and implementation more accessible to me, but I'm responsible for the problems in what was submitted and how I approached the community.
>
> I acknowledge the substantive feedback. I also hope OpenFisca will reflect on how it was expressed. The scope, deadline, submission volume, and use of tooling could all have been criticised directly. Inferring that the work was commercially motivated or that the account was an LLM, without first asking for clarification, introduced assumptions that weren't necessary to make those points.
>
> I've contributed some technical suggestions to the AI-policy RFC based on the incident: [RFC COMMENT LINK].
>
> I'll leave these issues and the PR closed. No response or further work is requested.
