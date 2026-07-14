# PIC Consumers

## Active Consumers

| Contract | Version | Consumer | Track | Status | Notes |
|---|---:|---|---|---|---|
| `pic-semantics` | `0.1.0` | `edithatogo/foi-o` | `oia_rules_20260704` | Active | Shared value states for OIA clock and process-rule invocation outputs. |
| `pic-crosswalk` | `0.1.0` | `edithatogo/foi-o` | `oia_rules_20260704` | Active | Maps OIA concepts and decisions to stable PIC IDs. |
| `pic-parameters` | `0.1.0` | `edithatogo/foi-o` | `oia_rules_20260704` | Active | Carries OIA limits and calendar references. |
| `pic-fixtures` | `0.1.0` | `edithatogo/foi-o` | `oia_rules_20260704` | Active | Candidate OIA deadline fixtures pending human curation. |
| `pic-traces` | `0.1.0` | `edithatogo/foi-o` | `oia_rules_20260704` | Active | Decision-trace shape for rule invocation results. |
| `pic-foio-compatibility` | `0.1.0` | `edithatogo/foi-o` | `foi_programme_governance_20260714` | Active | Optional release handshake; FOI-O remains runtime-authoritative. |

## Potential Consumers

| Contract | Version | Consumer | Track | Status | Notes |
|---|---:|---|---|---|---|
| `pic-traces` | `0.1.0` | `PolicyEngine` | `axiom_validation_20260706` | Potential | Trace export and missingness feedback is staged but still requires maintainer submission. |
| `pic-traces` | `0.1.0` | `OpenFisca` | `pic_v02_20260706` | Potential | Missingness feedback is staged but not yet submitted upstream. |
| `pic-parameters` | `0.1.0` | `DBN` | `adoption_closure_20260706` | Potential | Decimal-string guidance is staged as external proof. |
| `pic-crosswalk` | `0.1.0` | `Alaveteli` | `community_20260704` | Potential | Request-state taxonomy mapping is useful evidence but not an active PIC consumer yet. |
