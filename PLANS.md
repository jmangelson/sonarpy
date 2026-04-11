# Implementation Plan for Synthetic Aperture Sonar Notebook Curriculum

## 1. Purpose

This document turns the requirements in [SPEC.md](./SPEC.md) into a concrete implementation plan. It is intended to guide development from an empty project directory to a usable notebook-based educational package for signal processing, beamforming, and synthetic aperture sonar (SAS).

The plan is organized to preserve pedagogical progression, reduce rework, and ensure that shared code evolves alongside the notebook curriculum rather than being retrofitted at the end.

## 2. Implementation Principles

The implementation should follow these principles throughout:

- Build the curriculum in the same order that a learner will study it.
- Keep simulations simple before adding realism.
- Promote reusable code only when duplication becomes meaningful.
- Verify visual and conceptual clarity at every stage, not only numerical correctness.
- Make tradeoff discussions part of the implementation definition of done.
- Prefer a minimal, stable Python stack over premature tooling complexity.

## 3. Overall Delivery Strategy

The project should be implemented in the order defined later in Section 14, "Suggested Order of Actual Implementation Work." In practice, that means building the reusable helper library incrementally alongside the notebooks that first need it, rather than fully implementing every helper module up front.

The working sequence is:

1. Repository and environment setup
2. Plotting helpers and notebook utilities
3. DSP helpers needed for notebooks 1 through 5
4. Notebooks 1 through 5
5. Refactoring driven by duplication discovered during notebook work
6. `sonar.py` and notebooks 6 through 8
7. `arrays.py` and notebooks 9 through 11
8. `sas.py` and notebooks 12 through 15
9. Notebook 16 after the pipeline and parameter hooks are stable
10. Cleanup, cross-linking, and validation

Each step should produce working artifacts that can be reviewed independently.

## 4. Proposed Project Structure

Target structure:

```text
SonarPy/
  SPEC.md
  PLANS.md
  README.md
  pyproject.toml
  notebooks/
    01_signals_systems_and_sampling.ipynb
    02_sinusoids_complex_exponentials_and_phase.ipynb
    03_fourier_transform_and_spectral_intuition.ipynb
    04_convolution_filtering_and_matched_filters.ipynb
    05_noise_detection_and_estimation.ipynb
    06_sonar_basics_propagation_and_time_of_flight.ipynb
    07_chirps_pulse_compression_and_range_resolution.ipynb
    08_target_scene_modeling_and_echo_synthesis.ipynb
    09_array_geometry_and_spatial_sampling.ipynb
    10_conventional_beamforming.ipynb
    11_beamforming_tradeoffs_and_practical_effects.ipynb
    12_synthetic_aperture_intuition.ipynb
    13_sas_signal_model_and_phase_history.ipynb
    14_sas_focusing_and_image_formation.ipynb
    15_sas_pipeline_end_to_end.ipynb
    16_design_tradeoffs_and_development_decisions.ipynb
    _bootstrap.py
  src/
    sonar_py_lib/
      __init__.py
      dsp.py
      sonar.py
      arrays.py
      sas.py
      plotting.py
      notebook_utils.py
  data/
    generated/
  figures/
  tests/
    test_dsp.py
    test_sonar.py
    test_arrays.py
    test_sas.py
```

## 5. Stage 1: Repository and Environment Setup

### Objective

Create the initial project skeleton, dependency definition, and top-level documentation so notebook development happens in a stable environment.

### Tasks

1. Create the directory structure described above.
2. Add a `README.md` that explains:
   - project purpose,
   - notebook progression,
   - environment setup,
   - how to run notebooks in order.
3. Choose the environment definition format.
   - Preferred default: `pyproject.toml`
   - Optional alternative only if justified: `environment.yml`
4. Add baseline dependencies:
   - `jupyterlab`
   - `numpy`
   - `scipy`
   - `matplotlib`
   - `ipywidgets`
   - `pytest`
5. Add a lightweight package layout under `src/sonar_py_lib/`.
6. Ensure notebooks can import from `src/` cleanly.
7. Add a simple formatting and execution convention for notebooks.

### Deliverables

- Directory skeleton
- `README.md`
- `pyproject.toml`
- Package initialization files

### Exit Criteria

- Environment installs cleanly.
- Jupyter launches locally.
- A notebook can import from `sonar_py_lib`.

## 6. Stage 2: Early Shared Helper Foundation

### Objective

Build only the shared helper functionality needed to support the early DSP notebooks without over-abstracting too early.

### Tasks

1. Implement `plotting.py`:
   - waveform plots,
   - spectrum plots,
   - heatmaps,
   - beam pattern plots,
   - image display helpers.
2. Implement `dsp.py`:
   - signal generation,
   - sampling helpers,
   - FFT wrappers,
   - convolution,
   - correlation,
   - matched filter helper,
   - SNR utility functions.
3. Implement `notebook_utils.py`:
   - seeded randomness helpers,
   - consistent plotting style,
   - display helpers for assumptions and key takeaways.
4. Add unit tests for reusable math-heavy functions used by the early DSP material.

The later helper modules should be implemented when their notebook phases begin:

- `sonar.py` during notebooks 6 through 8
- `arrays.py` during notebooks 9 through 11
- `sas.py` during notebooks 12 through 15

### Deliverables

- Initial DSP, plotting, and notebook helper modules
- Basic test coverage for stable numerical utilities

### Exit Criteria

- Helpers support notebooks 1 through 5.
- Simple unit tests pass.
- Functions are named and documented consistently.

## 7. Stage 3: Phase 1 Notebooks - DSP Fundamentals

### Objective

Create the conceptual foundation required before introducing sonar-specific content.

### Notebook Order and Tasks

#### Notebook 01: Signals, Systems, and Sampling

Tasks:

1. Explain continuous vs discrete signals with simple examples.
2. Demonstrate sampling at multiple rates.
3. Show aliasing with under-sampled sinusoids.
4. Add quantization examples at different bit depths.
5. Include tradeoff discussion:
   - sample rate vs fidelity,
   - quantization vs storage and noise.

Done when:

- Plots clearly show aliasing behavior.
- Learner can explain Nyquist intuition in plain language.

#### Notebook 02: Sinusoids, Complex Exponentials, and Phase

Tasks:

1. Introduce sinusoid parameters and phase shifts.
2. Show complex exponential representation.
3. Visualize phasor rotation.
4. Connect phase to time delay.
5. Include tradeoff discussion:
   - interpretability of real sinusoids vs utility of complex form.

Done when:

- Learner can connect phase to later beamforming and SAS coherence concepts.

#### Notebook 03: Fourier Transform and Spectral Intuition

Tasks:

1. Introduce DFT/FFT numerically rather than abstractly first.
2. Show finite observation effects and leakage.
3. Compare window functions.
4. Sweep observation length and show resolution tradeoffs.
5. Include tradeoff discussion:
   - time resolution vs frequency resolution,
   - leakage vs window broadening.

Done when:

- Spectrum plots expose practical interpretation issues, not only theory.

#### Notebook 04: Convolution, Filtering, and Matched Filters

Tasks:

1. Explain impulse response and convolution with intuitive diagrams.
2. Show low-pass filtering effects.
3. Introduce correlation vs convolution.
4. Demonstrate matched filtering on simple pulses.
5. Include tradeoff discussion:
   - noise suppression vs distortion,
   - detection gain vs model mismatch.

Done when:

- Learner can see why matched filtering matters for sonar.

#### Notebook 05: Noise, Detection, and Estimation

Tasks:

1. Simulate noisy observations.
2. Show SNR impacts on detectability.
3. Demonstrate thresholding and false alarm tradeoffs.
4. Include simple parameter estimation examples.
5. Include tradeoff discussion:
   - sensitivity vs robustness,
   - false positives vs missed detections.

Done when:

- The notebook builds intuition for noisy sensor data before sonar modeling starts.

### Deliverables

- Five complete foundational notebooks
- Reusable DSP plotting and helper code validated in practice

### Exit Criteria

- All five notebooks run in sequence.
- Cross-notebook notation is consistent.
- Every notebook ends with recap and next-step framing.

## 8. Stage 4: Phase 2 Notebooks - Sonar and Ranging

### Objective

Map core DSP ideas into sonar-specific signal generation and echo interpretation.

### Notebook Order and Tasks

#### Notebook 06: Sonar Basics, Propagation, and Time of Flight

Tasks:

1. Introduce simple monostatic sonar geometry.
2. Model time-of-flight from range.
3. Simulate point-target returns.
4. Visualize transmit pulse and received echo delays.
5. Include tradeoff discussion:
   - timing resolution,
   - range ambiguity,
   - assumptions of constant sound speed.

#### Notebook 07: Chirps, Pulse Compression, and Range Resolution

Tasks:

1. Introduce chirps and bandwidth.
2. Simulate raw chirp echoes.
3. Apply matched filtering.
4. Compare compressed and uncompressed range response.
5. Sweep bandwidth and pulse duration.
6. Include tradeoff discussion:
   - energy vs resolution,
   - sidelobes vs mainlobe width.

#### Notebook 08: Target Scene Modeling and Echo Synthesis

Tasks:

1. Model scenes with multiple point targets.
2. Generate synthetic echoes from multiple delays and amplitudes.
3. Show overlap and ambiguity effects.
4. Optionally introduce simple reflectivity scaling.
5. Include tradeoff discussion:
   - scene complexity vs interpretability,
   - realism vs educational clarity.

### Deliverables

- Three sonar-focused notebooks
- Reusable range and echo synthesis helpers

### Exit Criteria

- Learner can simulate and interpret basic sonar returns.
- The project has a stable toy echo generator for later notebooks.

## 9. Stage 5: Phase 3 Notebooks - Arrays and Beamforming

### Objective

Build spatial processing intuition needed before synthetic aperture concepts are introduced.

### Notebook Order and Tasks

#### Notebook 09: Array Geometry and Spatial Sampling

Tasks:

1. Explain array element positions and look direction.
2. Show phase differences across sensors.
3. Simulate spatial aliasing and grating lobes.
4. Sweep element spacing and wavelength.
5. Include tradeoff discussion:
   - aperture size,
   - spacing constraints,
   - hardware complexity.

#### Notebook 10: Conventional Beamforming

Tasks:

1. Introduce delay-and-sum beamforming.
2. Build beam patterns for simple arrays.
3. Show effect of aperture on angular resolution.
4. Compare broadside and steered beams.
5. Include tradeoff discussion:
   - resolution vs sidelobes,
   - steering accuracy vs robustness.

#### Notebook 11: Beamforming Tradeoffs and Practical Effects

Tasks:

1. Add weighting/tapering examples.
2. Inject phase and gain errors.
3. Show beam degradation due to mismatch.
4. Connect coherence requirements to later SAS processing.
5. Include tradeoff discussion:
   - sidelobe suppression vs resolution loss,
   - calibration burden vs performance.

### Deliverables

- Three array and beamforming notebooks
- Stable array geometry and beam pattern utilities

### Exit Criteria

- Learner understands how phase, spacing, and aperture shape spatial resolution.
- Beamforming limitations are visible through simulation rather than only prose.

## 10. Stage 6: Phase 4 Notebooks - Synthetic Aperture Sonar

### Objective

Introduce SAS as an extension of coherent spatial processing and develop a simplified but defensible end-to-end pipeline.

### Notebook Order and Tasks

#### Notebook 12: Synthetic Aperture Intuition

Tasks:

1. Explain physical aperture limits.
2. Show how platform motion synthesizes a larger aperture.
3. Demonstrate coherent accumulation at a conceptual level.
4. Compare unfocused accumulation with coherent focusing.
5. Include tradeoff discussion:
   - path length,
   - coherence requirements,
   - motion sensitivity.

#### Notebook 13: SAS Signal Model and Phase History

Tasks:

1. Define a simple SAS geometry and coordinate system.
2. Simulate platform positions and target returns over aperture positions.
3. Visualize phase history for one or more targets.
4. Show consequences of along-track undersampling.
5. Include tradeoff discussion:
   - sampling density,
   - motion knowledge,
   - coherence retention.

#### Notebook 14: SAS Focusing and Image Formation

Tasks:

1. Choose a first image formation method.
   - Preferred starting point: backprojection or a simplified backprojection-style method.
2. Form a toy image from simulated phase history.
3. Compare focused vs defocused outputs.
4. Sweep aperture length and other key parameters.
5. Include tradeoff discussion:
   - compute cost vs interpretability,
   - focusing quality vs model assumptions.

#### Notebook 15: SAS Pipeline End to End

Tasks:

1. Assemble a complete toy pipeline:
   - transmit waveform,
   - echo generation,
   - matched filtering,
   - beam or aperture processing,
   - image formation.
2. Add configurable target scenes.
3. Inject selected errors:
   - motion error,
   - timing error,
   - phase instability,
   - undersampling.
4. Trace how errors propagate to the final image.
5. Include tradeoff discussion:
   - model simplicity vs realism,
   - accuracy vs computational load.

### Deliverables

- Four SAS-focused notebooks
- Toy end-to-end SAS processing framework

### Exit Criteria

- The learner can run a simplified SAS pipeline from raw simulated measurements to focused output.
- The connection between beamforming intuition and SAS image formation is explicit.

## 11. Stage 7: Phase 5 Notebook - Design Tradeoffs and Development Decisions

### Objective

Cap the curriculum with a notebook devoted to engineering judgment and parameter trade studies.

### Notebook 16 Tasks

1. Gather the most important parameters into a small set of repeatable experiments.
2. Compare changes in:
   - bandwidth,
   - aperture length,
   - element spacing,
   - sampling density,
   - noise level,
   - motion error.
3. Produce side-by-side output comparisons.
4. Summarize the practical consequences of each parameter choice.
5. Distinguish fundamental limits from implementation-specific choices.
6. Include recommendations on what to vary first when debugging poor image quality.

### Deliverables

- Final trade-study notebook

### Exit Criteria

- A learner can use the notebook as a design reference rather than only a tutorial.

## 12. Cross-Cutting Documentation Tasks

These tasks should happen continuously, not only at the end.

1. Maintain consistent notation across all notebooks.
2. Add a brief glossary or terminology table to the `README.md` or a future appendix.
3. Cross-link notebooks where concepts build directly.
4. Keep assumptions visible in notebook introductions.
5. Record known simplifications and omitted physics.

## 13. Testing and Validation Plan

### Code Validation

1. Add unit tests for deterministic helper functions.
2. Validate key formulas with simple sanity checks.
3. Confirm seeded simulations remain reproducible.

### Notebook Validation

1. Execute notebooks in order from a clean environment.
2. Check that plots render without manual fixes.
3. Confirm each notebook can be understood independently after the prerequisite list is read.
4. Review outputs for misleading scales, labels, or coordinate conventions.

### Pedagogical Validation

1. Verify each notebook states why the topic matters.
2. Verify each notebook includes at least one tradeoff section.
3. Verify each notebook includes a recap and next-step section.
4. Verify the transition between phases feels natural.

## 14. Suggested Order of Actual Implementation Work

The recommended build order is:

1. Create repository skeleton and environment definition.
2. Implement plotting helpers and notebook utilities first.
3. Implement `dsp.py` helpers needed for notebooks 1 through 5.
4. Build notebooks 1 through 5 completely.
5. Refactor duplicated code discovered during notebook development.
6. Implement `sonar.py` and notebooks 6 through 8.
7. Implement `arrays.py` and notebooks 9 through 11.
8. Implement `sas.py` and notebooks 12 through 15.
9. Build notebook 16 after the pipeline and parameter hooks are stable.
10. Run full cleanup, cross-linking, and validation pass.

This order is preferred because it follows the teaching progression while limiting speculative abstractions.

This section is the authoritative implementation sequence for the project. Earlier sections should be interpreted in a way that supports this order.

## 15. Definition of Done for Each Notebook

A notebook is complete only when all of the following are true:

- It has a clear title, purpose, prerequisites, and learning objectives.
- Core theory is introduced with plain-language interpretation.
- At least one simulation runs end to end.
- At least one meaningful visualization supports the lesson.
- Assumptions and simplifications are stated explicitly.
- Tradeoffs and failure modes are discussed.
- The notebook ends with a recap and suggested next questions.
- The notebook executes without hidden state dependencies.

## 16. Risks and Mitigations

### Risk: Overengineering Shared Code Too Early

Mitigation:

- Keep helper modules small and notebook-driven.
- Refactor only after at least two notebooks need the same logic.

### Risk: Notebooks Become Too Long

Mitigation:

- Split advanced material into later notebooks rather than expanding early ones indefinitely.
- Keep one central teaching objective per notebook.

### Risk: SAS Content Becomes Too Abstract

Mitigation:

- Use repeated visual links back to sampling, phase, filtering, and beamforming.
- Show intermediate representations, not only final images.

### Risk: Simulations Are Too Slow for Iteration

Mitigation:

- Start with tiny scenes and simplified geometries.
- Add optional higher-resolution cells only where useful.

### Risk: Tradeoff Discussions Drift Into Vague Prose

Mitigation:

- Tie each tradeoff discussion to parameter sweeps or comparative plots.
- Require visible examples of what improves and what gets worse.

## 17. Immediate Next Actions

The first concrete implementation actions should be:

1. Create the directory skeleton under the repository root.
2. Add `README.md`.
3. Add `pyproject.toml`.
4. Create the `src/sonar_py_lib/` package with placeholder modules.
5. Create empty or minimally scaffolded notebook files for all 16 planned notebooks.
6. Implement shared plotting, notebook utility, and DSP helpers needed for notebooks 1 through 3.
7. Draft notebook 1 before touching any sonar-, array-, or SAS-specific code.
8. Continue notebook development through notebook 5 before implementing `sonar.py`.

## 18. Concrete Backlog

Use this backlog as the working checklist. Each notebook must be verified before moving on to the next one.

### Per-Notebook Verification Checklist

Every `Verify notebook N` step in this section should include all of the checks below before the notebook is considered complete.

1. Execution verification
   - Execute the notebook end to end from a clean kernel.
   - Confirm every code cell runs without manual intervention.
   - Confirm imports, helper functions, and package paths work in the intended environment.
   - Confirm printed outputs and derived values are numerically plausible for the scenario being taught.

2. Technical correctness verification
   - Confirm equations, definitions, and parameter values match the intended concept.
   - Confirm plotted data matches the explanation in the markdown text.
   - Confirm sign conventions, units, coordinate conventions, and indexing choices are internally consistent.
   - Confirm tradeoff statements are supported by visible examples, not only prose.

3. Figure and visualization verification
   - Inspect rendered figure images directly, not only the plotting code.
   - Confirm legends do not cover important data and are placed intentionally.
   - Confirm axis labels, titles, units, tick labels, and font sizes are readable.
   - Confirm line colors, marker styles, and contrast make overlaid signals distinguishable.
   - Confirm subplot spacing, aspect ratios, and margins are adequate.
   - Confirm annotations and callouts do not overlap with plotted content.
   - Confirm heatmaps, images, and colorbars use readable scales and labels.
   - Confirm figures communicate the intended lesson without requiring code inspection to interpret them.

4. Pedagogical verification
   - Confirm the notebook states its purpose and learning objective clearly.
   - Confirm the notebook introduces concepts in the intended progression from simple to more complex.
   - Confirm new terminology is defined before or at first meaningful use, either inline or in a short terminology section.
   - Confirm abbreviations are expanded at first use, even when that first use occurs in the terminology section.
   - Confirm notebooks introducing major new concepts include a "Mathematical Definitions and Relevant Intuition" section where appropriate.
   - Confirm mathematical concepts and equations cite concrete references where appropriate.
   - Confirm inline mathematical citations name the source directly, for example "Wikipedia Matched Filter article", rather than using vague phrases.
   - Confirm the purpose of each major figure or animation is described before that visual is referenced or interpreted in surrounding markdown.
   - Confirm text before a figure or animation states the intended lesson of the visual and may point out what the learner should look at to understand it.
   - Confirm text after a figure or animation helps the learner interpret the visual, connect its components to the concept, and understand the lesson being taught.
   - Confirm text around a figure or animation does not describe how the visual was revised, improved, or constructed for teaching purposes.
   - Confirm assumptions and simplifications are stated explicitly.
   - Confirm the notebook includes at least one meaningful simulation and visualization.
   - Confirm the notebook includes a tradeoffs or limitations section.
   - Confirm the notebook ends with a recap and suggested next questions or next steps.

5. Reusability and helper-layer verification
   - Confirm duplicated logic is only promoted into shared helpers when it is genuinely reusable.
   - Confirm helper APIs used by the notebook are stable, named clearly, and still minimal.
   - Confirm notebook-specific teaching code remains in the notebook unless reuse is justified.
   - Confirm any helper changes required by verification are covered by tests where practical.

6. Sequence verification
   - Confirm notation, terminology, and assumptions remain consistent with earlier notebooks.
   - Confirm the notebook can be understood after reading only its stated prerequisites.
   - Confirm the transition to the next notebook is explicit and accurate.

7. Preliminary git checkpoint
   - Create a preliminary git commit for the notebook and any directly related helper or documentation updates after technical and pedagogical verification are in good shape.
   - Push that preliminary state before requesting human review so the review is tied to a concrete shared revision.
   - Make it explicit in the commit message that the notebook is still pending final verification or approval.

8. Final user verification
   - Present the rendered notebook to the user for review after technical verification and the preliminary push are complete.
   - Ask the user to check explanation quality, figure readability, legend placement, and teaching clarity.
   - Record any user-requested fixes before marking the notebook verified.
   - Do not begin the next notebook until the user confirms the current notebook is acceptable.

9. Final approval git checkpoint
   - After user feedback is resolved and the notebook is approved, commit the final accepted notebook state.
   - Push that final approved state so `main` reflects the notebook revision that passed human verification.
   - Only then mark the notebook verified and move on to the next notebook.

### Tracking Checklist

- [x] Verify notebook 1 end to end.
- [x] Fix any notebook 1 issues found during verification.
- [x] Stabilize `plotting.py`, `notebook_utils.py`, and `dsp.py` only where notebook 1 verification exposes gaps.
- [x] Build notebook 2 completely.
- [x] Verify notebook 2 before starting notebook 3.
- [x] Fix any notebook 2 issues found during verification.
- [x] Build notebook 3 completely.
- [x] Verify notebook 3 before starting notebook 4.
- [x] Fix any notebook 3 issues found during verification.
- [x] Build notebook 4 completely.
- [x] Verify notebook 4 before starting notebook 5.
- [x] Fix any notebook 4 issues found during verification.
- [x] Build notebook 5 completely.
- [x] Verify notebook 5 before Phase 1 refactoring.
- [x] Fix any notebook 5 issues found during verification.
- [x] Review duplicated Phase 1 code only after notebooks 1 through 5 are complete and verified, and refactor only if it clearly improves reuse without hurting notebook clarity.
- [x] Validate notebooks 1 through 5 as a complete sequence from a clean environment.
- [ ] Implement `sonar.py` only after Phase 1 is complete and stable.
- [ ] Build notebook 6 completely.
- [ ] Verify notebook 6 before starting notebook 7.
- [ ] Fix any notebook 6 issues found during verification.
- [ ] Build notebook 7 completely.
- [ ] Verify notebook 7 before starting notebook 8.
- [ ] Fix any notebook 7 issues found during verification.
- [ ] Build notebook 8 completely.
- [ ] Verify notebook 8 before moving to `arrays.py`.
- [ ] Fix any notebook 8 issues found during verification.
- [ ] Implement `arrays.py` only after notebooks 6 through 8 are complete and stable.
- [ ] Build notebook 9 completely.
- [ ] Verify notebook 9 before starting notebook 10.
- [ ] Fix any notebook 9 issues found during verification.
- [ ] Build notebook 10 completely.
- [ ] Verify notebook 10 before starting notebook 11.
- [ ] Fix any notebook 10 issues found during verification.
- [ ] Build notebook 11 completely.
- [ ] Verify notebook 11 before moving to `sas.py`.
- [ ] Fix any notebook 11 issues found during verification.
- [ ] Implement `sas.py` only after notebooks 9 through 11 are complete and stable.
- [ ] Build notebook 12 completely.
- [ ] Verify notebook 12 before starting notebook 13.
- [ ] Fix any notebook 12 issues found during verification.
- [ ] Build notebook 13 completely.
- [ ] Verify notebook 13 before starting notebook 14.
- [ ] Fix any notebook 13 issues found during verification.
- [ ] Build notebook 14 completely.
- [ ] Verify notebook 14 before starting notebook 15.
- [ ] Fix any notebook 14 issues found during verification.
- [ ] Build notebook 15 completely.
- [ ] Verify notebook 15 before starting notebook 16.
- [ ] Fix any notebook 15 issues found during verification.
- [ ] Build notebook 16 completely.
- [ ] Verify notebook 16 as the final curriculum capstone.
- [ ] Fix any notebook 16 issues found during verification.
- [ ] Run full cleanup, cross-linking, glossary, and end-to-end validation pass.

## 19. Success Checkpoints

Use these checkpoints to evaluate progress:

### Checkpoint A

- Environment is runnable.
- Package imports work.
- Plotting and notebook utility helpers are in place.
- Notebook 1 is complete.

### Checkpoint B

- `dsp.py` plus the early shared helper layer are stable.
- Notebooks 1 through 5 are complete and coherent.
- Refactoring of duplicated Phase 1 code has been completed where useful.

### Checkpoint C

- `sonar.py` is implemented and notebooks 6 through 8 are complete.
- `arrays.py` is implemented and notebooks 9 through 11 are complete.
- Sonar and array simulations are reusable and understandable.

### Checkpoint D

- `sas.py` is implemented.
- Notebooks 12 through 15 demonstrate a working toy SAS pipeline.

### Checkpoint E

- Notebook 16 is complete.
- Full curriculum has been run and reviewed end to end.

## 20. Final Outcome

When this plan is completed, the project should provide a stepwise notebook curriculum that starts from basic DSP intuition and ends with a meaningful, simulation-backed understanding of the synthetic aperture sonar processing pipeline and its main engineering tradeoffs.
