# Measurement And Claim Checks

Read only the section relevant to the decision. These are interpretation checks, not replacements for the measurement skills' processing workflows or acceptance rules.

## Claim-Level Audit

For every conclusion that would change an experiment or manuscript claim, establish:

- The exact observation, its primary-source or raw-file locator, and what was actually inspected.
- The material, preparation history, cell/test conditions, and scope over which the claim holds.
- The strongest credible alternative or confounder, and whether existing evidence distinguishes it.
- The arithmetic/model assumptions, if the claim depends on a derived value.
- Wording proportional to the evidence and a next observation that could revise it.

Apply these to decisive claims, not every background sentence. If evidence is incomplete, say whether the claim is supported within stated conditions, provisional, or not established and give the reason. Do not generate numerical confidence percentages without a defensible statistical basis.

## Numbers And Comparisons

- Verify source value, unit, sign, axis/reference scale, active-mass basis, area, thickness, and denominator as applicable. Keep recorded settings separate from recomputed theoretical values.
- Check C-rate definitions before translating C into current. Do not silently replace a historical capacity basis with a formula-derived value. State the formula, input values, and material/composition assumptions for consequential calculations.
- Check retention baseline/cycle identity and charge/discharge direction for CE. Distinguish an absolute capacity change, relative retention, and a percentage-point change.
- Compare performance only after aligning voltage window/reference, cell configuration, loading, temperature, pressure, electrolyte, carbon fraction, and cycle/rate protocol where they affect interpretation. Otherwise report a conditional comparison.
- Check dimensional consistency and order of magnitude. Recompute decision-changing values directly from original inputs. Carry uncertainty from repeatability, digitization, fitting, or assumed parameters; do not invent precision or repeats.

## EIS And DRT

Use an appropriate EIS/DRT specialist workflow for raw-data processing when available.

- Verify frequency/unit/imaginary-sign conventions, raw points, excluded records, and measurement conditions before assigning processes.
- Assess repeats, AC-amplitude dependence, and rest/stationarity controls when scientific acceptance depends on them. A KK screen pass alone does not establish all those properties. Preserve the modality workflow's acceptance status; do not promote `screen-pass` to full acceptance or clear `controls-incomplete-no-acceptance` without the missing controls.
- Equivalent circuits and DRT are model-dependent representations. Fit quality or a peak does not uniquely identify a physical process. Use independent perturbations or controls to support an assignment.
- Check frequency-supported time ranges, regularization/model sensitivity, and inductive behavior through the specialist workflow. Do not interpret unsupported tails or force every feature into an RC process.

## CV, GCD, And GITT

Use an appropriate battery analysis workflow for raw-data parsing and calculations.

- CV peak changes, b-values, and capacitive fits require the proper scan/cycle window and fit conditions; they alone do not identify a unique storage mechanism.
- Separate reversible capacity, rate behavior, first-cycle loss, CE, retention, polarization, and energy efficiency. One improvement does not establish all-around or practical-cell performance.
- For GITT, verify pulse/rest pairing, relaxation, suitable fitting intervals, geometry/mass inputs, and the model assumptions before reporting diffusion values. Do not promote an apparent diffusion estimate to an intrinsic coefficient without support.
- Preserve raw files and the exclusion reason when the user asks to ignore erroneous data. An excluded point is not a deleted source or evidence of a verified mechanism.

## Structure, Defects, And DFT

- No detected XRD impurity peak is a detection-limited observation, not absolute phase purity. A lattice shift may have several structural or instrumental causes; judge refinement validity and complementary evidence through the relevant XRD skills.
- Distinguish unit-cell volume change over a measured state-of-charge range from macroscopic electrode strain. Match lithiation range, phase fractions, uncertainty, and reversibility before using zero-strain language.
- A valence or XPS peak change alone does not uniquely establish oxygen vacancies or their causal role. Check composition, charge balance, plausible compensation routes, and independent defect evidence.
- Use an appropriate DFT workflow for computations. Identify the representative structure, composition, configuration, method, convergence, reference states, and chemical potentials needed by the actual claim. Formation energy, defect energy, migration barrier, and phonon stability answer different questions.
- Progress or completed force calculations do not establish phonon stability. A favorable result for one model is bounded to that model and its approximations. If the user wants only to show possibility, design the smallest falsifiable proxy and state its limit.

## Solid Electrolytes And Practical Transfer

- Distinguish ionic/electronic conductivity, chemical compatibility, electrochemical stability, interfacial passivation, moisture response, and mechanical contact. A small measured current or stable visual appearance does not by itself establish thermodynamic stability.
- Separate lithium-metal, anode, cathode, carbon-additive, and air/moisture interactions. Check electrode configuration, pressure, surface/handling history, and time dependence for the proposed compatibility claim.
- Liquid half cells, symmetric cells, pressed pellets, and practical full cells constrain different questions. Bound extrapolations by loading, electrolyte amount, electrode formulation, balancing, pressure, and cycling conditions.

## Minimal Discriminating Control

Choose the fastest feasible test whose outcomes differ between leading explanations. Specify the changed variable, matched controls, what is measured, and how a positive, negative, or unresolved result would affect the claim. Set quantitative acceptance limits from the actual protocol, uncertainty, or cited method; do not invent universal thresholds.

For costly follow-up experiments, prefer a staged decision: first test the uncertain premise, then expand only if its result justifies the next step. More characterization is not automatically better evidence if it cannot distinguish the explanations.
