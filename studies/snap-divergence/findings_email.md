Subject: SNAP Divergence Study Results - PolicyEngine vs. Atlanta Fed PRD

Dear Rules-as-Code Community of Practice,

We have completed a systematic, differential-testing evaluation comparing the Supplemental Nutrition Assistance Program (SNAP) implementations in PolicyEngine (Python) and the Atlanta Fed Policy Rules Database (PRD, R) for Federal Fiscal Year 2026.

Our findings indicate a high level of reliability and agreement between the two independent models:
1. Across a suite of 50 human-curated golden fixtures representing California, Texas, Pennsylvania, Mississippi, and Georgia scenarios, we achieved a 100% output agreement rate on both eligibility status and allotment amounts.
2. We identified 15 structural divergences representing differences in modeling scope (e.g., direct SNAP eligibility gates in PRD vs. PolicyEngine's emulation of the TANF non-cash categorical eligibility pathway), utility deduction triggers, and parameter vintages, which we have cataloged and classified. No code-level bugs were found in either engine.

The full study artifacts, including the runners, the crosswalk schema, the fixture corpus, and our detailed paper draft, are available in our repository:
https://github.com/edithatogo/rulesandprocesses/tree/main/studies/snap-divergence/

We look forward to discussing these results and exploring how systematic differential testing can be adopted as a standard practice for public-benefit Rules-as-Code projects.

Best regards,
Dylan & Antigravity
