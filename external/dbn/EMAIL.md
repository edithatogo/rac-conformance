# Email Pitch to Digital Benefits Network (DBN) Rules-as-Code CoP

**To:** rulesascode@georgetown.edu  
**From:** Dylan (Maintainer of `foi-o`)  
**Date:** July 2026

Dear Digital Benefits Network Rules-as-Code CoP,

My name is Dylan, and I am the maintainer of `foi-o` (the open-source Official Information Act processing engine for New Zealand) and a contributor to the PolicyEngine and Axiom ecosystems.

I am writing to share the findings of a systematic model-to-model validation study we recently conducted, which we believe directly addresses the **verification gap** identified in your *AI-Powered Rules as Code* report, as well as the need for an **open standard and shared code library** highlighted in your *Cross-Sector Insights* report.

We conducted a differential-testing study comparing the SNAP implementations in PolicyEngine (Python) and the Atlanta Fed Policy Rules Database (R) for Federal Fiscal Year 2026 across five states (CA, TX, PA, MS, GA). Our findings show:
1. **Perfect Agreement on Core Cases:** Across 50 human-curated golden fixtures, the two independent engines achieved a 100% agreement rate on eligibility and allotment values.
2. **Structural Divergences Documented:** We identified and classified 15 decision-relevant divergences (e.g., state-option BBCE routing and utility trigger differences) resulting from modeling scope and adapter differences rather than code-level programming bugs.

### Our Offer
We would be delighted to:
1. **Present our findings** and methodology at a future DBN Rules-as-Code CoP roundtable.
2. **Share the lightweight JSON format schemas** (Policy Interchange Contracts, or PIC) we designed to enable cross-engine verification of parameters, fixtures, and execution traces.

### Our Ask
We would love to know from the CoP:
- Which benefit programs or specific state-option combinations would you most like to see compared next using this differential validation harness?

The full study repo, including the R and Python runners and our draft paper, can be found here:
https://github.com/edithatogo/rulesandprocesses/tree/main/studies/snap-divergence/

Looking forward to hearing from you.

Best regards,  
Dylan & the Antigravity pair programmer
