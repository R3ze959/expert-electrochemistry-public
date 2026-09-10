# Deep Research Mode

Use for an explicit request for depth or a consequential question with competing explanations. Depth comes from discriminating evidence and independent checking, not answer length, a fixed paper count, or a claimed increase in reasoning tokens.

## Choose Effort By Uncertainty

- `deep-lite` / focused: resolve the main uncertainty with compact recall and targeted source checks. Delegate only when there is useful independent work.
- `deep`: build a compact evidence map, inspect decisive sources, compare alternative explanations, and use independent checks when delegation is available. External search is required for novelty/current claims or other live-verification needs.
- `systematic`: use a suitable literature-search workflow with explicit query families, databases, dates, inclusion criteria, deduplication, and coverage limits. Exhaustiveness is a search-scope claim, never established by a large hit count.

Choose initial retrieval size for readability, then expand only to fill identified gaps. Several inspected decisive studies can be more useful than dozens of loosely matched hits. Do not force a target number of papers, agents, or recommended directions.

## Investigate In Stages

1. **Frame the decision.** Identify what would change the user's experiment, interpretation, or manuscript wording. Capture the known system, constraints, raw observations, and important missing conditions. Make reasonable assumptions explicit and continue work that does not depend on missing inputs.
2. **Retrieve and triage.** Inspect relevant user-supplied sources and data; use compact recall only for a corpus explicitly placed in scope. Launch external search alongside local work when freshness, novelty, uncertainty, or the user's scope requires it. Separate candidate discovery from verified evidence.
3. **Make explanations testable.** For each credible hypothesis or route, identify a predicted observation, a confounder, and a result that would weaken it. Seek disconfirming or null findings as well as support. Include instrumentation, normalization, and sample-history explanations when relevant.
4. **Delegate independent work.** Read [astra-multi-agent.md](astra-multi-agent.md). Give agents bounded questions, evidence access, and return requirements. Keep synthesis and at least one substantive investigation on the main agent. Avoid sending the preferred conclusion to an independent evaluator.
5. **Resolve decisive uncertainties.** Open the relevant original pages/figures/methods and recalculate consequential values. Reconcile source versions and measurement conditions before treating papers as contradictory. Use [measurement-claim-checks.md](measurement-claim-checks.md) for the relevant domain checks.
6. **Synthesize and challenge.** Rank explanations by inspected support and ability to distinguish observations. Identify the strongest unresolved challenge. Recheck the source or calculation behind any agent result that changes the recommendation. Downgrade the claim if the evidence cannot distinguish alternatives.
7. **Deliver the decision.** Give the user the practical conclusion, the strongest evidence, the material limitation, and a feasible next control with an interpretable outcome. Continue through the requested deliverable rather than stopping after a plan.

## Evidence Map

Keep only the fields that help the decision; use a compact internal table or requested final artifact:

| Claim / hypothesis | Source and exact locator | Inspection status | System and conditions | Observation / normalization | Alternative or caveat | Effect on decision |
| --- | --- | --- | --- | --- | --- | --- |

A locator is a PDF page/figure/table, DOI plus an inspected section, or a raw-file path plus sheet/range or record. Record whether a value was reported, independently calculated, or estimated from a plot. Different citations describing the same experiment are one evidence source.

Confidence is a claim-level judgment with a reason, not a paper reputation score. Use qualitative terms when helpful; do not invent numerical probabilities or combine agent votes into confidence.

## Stop Or Escalate

Finish when:

- The requested breadth and output are covered.
- Evidence that controls the recommendation is inspected, or its unavailability is stated and the claim is bounded accordingly.
- Credible alternatives have been tested against available evidence; indistinguishable hypotheses remain explicitly unresolved.
- Consequential arithmetic, units, normalization, and source scope have been checked.
- The next control targets a remaining uncertainty and fits the user's constraints.

Expand only for an identified gap that could change the result. If another search route yields only duplicates or inaccessible records, report that limitation and choose a different source or experimental discriminator. Do not claim completion of a comprehensive search when required coverage is unavailable.
