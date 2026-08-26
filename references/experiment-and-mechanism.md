# Experiment, Statistics, and Mechanism Guidance

Use this reference for experiment design, failed-batch diagnosis, electrochemical interpretation, and mechanism claims.

## Build Competing Explanations

Start with two to five plausible explanations rather than one preferred story. For each, state:

- required physical or chemical change;
- observations explained and left unexplained;
- a unique or strongly discriminating prediction;
- the cheapest safe test that could falsify it;
- the result that would force a change in interpretation.

Rank explanations by fit to the full evidence, not novelty.

## Experimental Units and Replication

Before statistical interpretation, identify the experimental unit. Distinguish:

- independent material-synthesis batches;
- independently assembled cells or specimens;
- technical repeats from the same batch or specimen;
- repeated cycles, time points, pixels, or spectra from one unit.

Do not treat repeated observations from one unit as independent samples. Use blocking or hierarchical analysis when cells are nested within batches. Randomize assembly or measurement order when drift is plausible, predefine exclusion criteria, and report all exclusions.

Choose sample size from expected variability and the smallest decision-relevant effect, or label the study exploratory when that information is unavailable. Report effect sizes and confidence intervals; propagate measurement and normalization uncertainty when it can affect the conclusion.

## Minimum Useful Experiment Matrix

Prefer the smallest design that separates variables cleanly:

- baseline or untreated control;
- single-factor controls;
- combined treatment when interaction is claimed;
- processing blank when the route itself may change the sample;
- independent batches and specimens proportional to expected variability.

For factors A and B, the additive-scale interaction contrast is:

`I = Y_AB - Y_A - Y_B + Y_0`

Estimate interaction with a factorial or hierarchical model and an interval, not only a point difference. Confirm that the response scale is appropriate. A nonzero interaction supports non-additivity, not a microscopic mechanism by itself.

## Technique Validity Gates

Use a specialist workflow for full analysis; at minimum check:

- **CV:** cycle and scan-rate selection, baseline, iR treatment, loading/area, reference stability, and whether peak changes persist across matched replicates. Smaller peak separation means lower apparent polarization under the tested conditions; by itself it does not uniquely identify faster interfacial charge transfer.
- **GCD/cycling:** capacity basis, current definition, cutoff logic, formation, retention denominator, missing cycles, and cell/batch independence.
- **GITT/PITT:** complete pulse-rest pairing, adequate relaxation, local fit quality, geometry, thermodynamic factor assumptions, and whether the result is only an apparent transport metric.
- **EIS:** linearity, stability, frequency coverage, sign/units, Kramers–Kronig or equivalent consistency check, residual structure, parameter identifiability, and repeatability.
- **XRD/Rietveld:** background/peak-shape/model dependence, phase detection limits, preferred orientation, correlated parameters, fit residuals, and orthogonal composition evidence.
- **Spectroscopy/microscopy:** sampling depth, preparation artifacts, spatial representativeness, calibration, beam damage, and matched state of charge.
- **DFT:** modeled composition and ordering, convergence, functional and correction choices, reference states, finite-size effects, and whether the computed observable maps to the experimental claim.

When techniques disagree, check sampling depth, relaxation, specimen matching, exposure history, and the quantity each method actually measures.

## Fastest Discriminating Check

For a non-trivial mechanism or troubleshooting decision, end with one check that is fast, interpretable, and capable of changing the decision. State expected outcomes under each leading explanation, the decision criterion, and what remains unresolved if the test succeeds.

One screening result cannot establish a complete mechanism. Strong causality normally needs controlled perturbation, temporal ordering, orthogonal validation, and exclusion of credible alternatives.

## Safety Boundary

For reactive gases, toxic fluorine or sulfur species, active alkali metals, high pressure, high energy, or other hazardous work, do not provide an executable procedure unless the user has an approved institutional SOP and suitable facilities. Require current SDS review, engineering controls, monitoring, compatible materials, waste handling, emergency response, and trained supervision. When these cannot be verified, give only a high-level decision boundary and safer alternatives.
