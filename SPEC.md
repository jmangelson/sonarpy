# Synthetic Aperture Sonar Notebook Curriculum Specification

## 1. Purpose

This project will produce a structured set of Jupyter notebooks that progressively build from foundational signal processing concepts to beamforming, array processing, and the synthetic aperture sonar (SAS) signal processing pipeline.

The notebooks are intended to serve two roles:

1. A self-study and refresher resource for core signal processing concepts.
2. A practical, simulation-driven environment for understanding the tradeoffs, assumptions, and implementation decisions behind SAS processing systems.

The end state is a notebook collection that explains not only how the SAS pipeline works, but why specific processing choices are made and what is gained or lost when those choices change.

## 2. Goals

### Primary Goals

- Build intuition from first principles rather than starting from black-box algorithms.
- Connect mathematical concepts to concrete simulations and visualizations.
- Progress from simple 1D signal processing to 2D/3D spatial sensing and SAS-specific processing.
- Emphasize engineering tradeoffs, failure modes, and practical assumptions.
- Create material that is useful both for learning and for future reference.

### Secondary Goals

- Provide reusable code cells and helper utilities that support multiple notebooks.
- Make the notebooks easy to extend with more realistic models later.
- Keep the content rigorous enough to support implementation decisions in future prototypes.

## 3. Non-Goals

- This project is not initially intended to be a production-grade SAS processor.
- This project is not initially intended to cover every sonar modality or ocean acoustics topic in depth.
- This project is not initially intended to optimize for real-time execution.
- This project is not initially intended to provide a full survey of all beamforming or SAS research literature.

## 4. Target Audience

Primary audience: one technically capable learner with some prior exposure to math, physics, and software, who wants to rebuild deep intuition and working understanding.

Assumed background:

- Basic calculus and linear algebra
- Basic complex numbers and trigonometry
- Some Python familiarity
- Some prior exposure to Fourier analysis or signal processing terminology

The notebooks should still re-explain concepts clearly enough that they work as a refresher rather than assuming recent mastery.

## 5. Core Educational Philosophy

Each notebook should follow this pattern where possible:

1. State the problem in plain language.
2. Introduce the minimal theory required.
3. Show the governing equations and assumptions.
4. Simulate a simple case.
5. Visualize what changes as key parameters vary.
6. Explain practical tradeoffs and likely failure modes.
7. Connect the lesson to the next stage of the SAS pipeline.

The notebooks should prefer interpretability over compactness. Explanations, plots, and parameter sweeps are more important than clever code.

## 6. Functional Requirements

### Curriculum Requirements

- The project must include a sequenced notebook curriculum from beginner/intermediate signal processing to SAS pipeline understanding.
- The notebook ordering must be pedagogically progressive, with each notebook depending only on prior material or clearly stated prerequisites.
- Each notebook must include explicit learning objectives.
- Each notebook must include at least one simulation and at least one visualization.
- Each notebook must include a section on engineering tradeoffs or limitations.
- Each notebook must conclude with a short summary and suggested next questions.

### Content Requirements

The notebook set should cover, at minimum:

- Continuous vs discrete signals
- Sampling, aliasing, and quantization intuition
- Sinusoids, complex exponentials, and phasors
- Time-domain vs frequency-domain representations
- Convolution, filtering, impulse response, and matched filtering
- Correlation and detection intuition
- Noise models and signal-to-noise ratio
- Pulse compression and chirp signals
- Geometry of sensing, propagation delay, and range estimation
- Array fundamentals, phase differences, and spatial sampling
- Conventional beamforming and its limitations
- Resolution, ambiguity, sidelobes, and aperture tradeoffs
- Motion, coherent integration, and synthetic aperture intuition
- SAS image formation at a conceptual and simulation level
- Key pipeline stages in SAS processing and how upstream errors affect downstream products

### Engineering Requirements

- The notebooks must use Python.
- The notebooks should prefer standard scientific Python tools unless a strong reason exists otherwise.
- The notebooks should be executable locally in sequence.
- The notebooks should be readable even when not executed.
- Simulations should start simple and computationally cheap.
- More realistic models should be introduced only after the idealized case is understood.

## 7. Proposed Notebook Sequence

This sequence is the baseline plan. Titles may change, but the progression should remain similar.

### Phase 1: Signal Processing Foundations

1. `01_signals_systems_and_sampling.ipynb`
   - Signals, systems, sampling, aliasing, quantization
   - Time axis intuition and numerical representation

2. `02_sinusoids_complex_exponentials_and_phase.ipynb`
   - Sinusoids, Euler form, phase, frequency, superposition
   - Why complex representation matters

3. `03_fourier_transform_and_spectral_intuition.ipynb`
   - DFT/FFT intuition, leakage, windowing, spectral resolution
   - Tradeoff between observation length and frequency resolution

4. `04_convolution_filtering_and_matched_filters.ipynb`
   - LTI systems, impulse response, convolution, matched filtering
   - Detection and SNR gain intuition

5. `05_noise_detection_and_estimation.ipynb`
   - Noise models, SNR, thresholding, false alarms, estimation basics

### Phase 2: Sonar and Ranging Foundations

6. `06_sonar_basics_propagation_and_time_of_flight.ipynb`
   - Sound propagation assumptions, time-of-flight, range estimation
   - Simple point-target simulations

7. `07_chirps_pulse_compression_and_range_resolution.ipynb`
   - Chirp design, bandwidth, matched filtering, pulse compression
   - Range resolution tradeoffs

8. `08_target_scene_modeling_and_echo_synthesis.ipynb`
   - Scene primitives, reflectivity, delayed returns, multipath simplifications

### Phase 3: Arrays and Beamforming

9. `09_array_geometry_and_spatial_sampling.ipynb`
   - Linear arrays, element spacing, grating lobes, steering vectors

10. `10_conventional_beamforming.ipynb`
    - Delay-and-sum beamforming
    - Beam patterns, sidelobes, aperture vs resolution

11. `11_beamforming_tradeoffs_and_practical_effects.ipynb`
    - Weighting, calibration errors, phase mismatch, platform uncertainty

### Phase 4: Synthetic Aperture Sonar

12. `12_synthetic_aperture_intuition.ipynb`
    - Physical aperture vs synthetic aperture
    - Platform motion and coherent integration

13. `13_sas_signal_model_and_phase_history.ipynb`
    - SAS geometry, phase history, along-track sampling requirements

14. `14_sas_focusing_and_image_formation.ipynb`
    - Backprojection or simplified image formation
    - Conceptual comparison of focusing approaches

15. `15_sas_pipeline_end_to_end.ipynb`
    - End-to-end toy pipeline from transmit signal to focused image
    - Error injection and sensitivity analysis

16. `16_design_tradeoffs_and_development_decisions.ipynb`
    - Parameter trade studies
    - Why different development choices exist
    - What breaks first when assumptions fail

## 8. Per-Notebook Structure Requirements

Each notebook should include:

- Title and short statement of purpose
- Prerequisites and links to earlier notebooks when relevant
- Learning objectives
- Definitions for new terms before or at first meaningful use, either inline or in a short terminology section
- Conceptual overview
- Core equations with plain-language interpretation
- One or more simulations
- Plots that expose parameter sensitivity
- Discussion of assumptions and limitations
- Short recap
- Suggested exercises or extensions

## 9. Simulation Requirements

The simulations should be layered by realism:

### Level 1: Idealized

- Noise-free
- Perfect timing
- Point targets
- Straight-line motion
- Uniform medium
- Perfect sensor calibration

### Level 2: Mildly Realistic

- Additive noise
- Finite bandwidth effects
- Simple sidelobes
- Limited aperture
- Modest motion perturbations

### Level 3: Stress Cases

- Calibration errors
- Motion estimation errors
- Undersampling in time or space
- Phase instability
- Model mismatch

The curriculum does not need to reach fully realistic ocean acoustics early, but it should make clear where the simplified models stop being reliable.

## 10. Visualization Requirements

The notebooks should heavily use visual explanations, including:

- Time-domain waveforms
- Spectra and spectrograms
- Correlation and matched-filter outputs
- Array geometry diagrams
- Beam patterns
- Range-angle maps where useful
- Phase history visualizations
- Focused vs defocused SAS imagery
- Parameter sweep heatmaps

Visuals should be used to explain tradeoffs, not merely decorate the notebooks.

## 11. Code Organization Requirements

The implementation should separate explanatory notebook code from reusable helper code where practical.

Proposed structure:

```text
SonarPy/
  SPEC.md
  PLANS.md
  README.md
  pyproject.toml
  notebooks/
  src/
    sonar_py_lib/
      dsp.py
      sonar.py
      arrays.py
      sas.py
      plotting.py
  data/
    generated/
  figures/
  tests/
```

Requirements:

- Shared utilities should live in `src/sonar_py_lib/`.
- Notebook-specific code should remain in notebooks unless it is clearly reusable.
- Notebooks should be runnable from a fresh checkout after installing the project in editable mode.
- Generated data and figures should be reproducible.
- Randomness should be seeded where reproducibility matters.

## 12. Tooling and Dependencies

Preferred baseline stack:

- Python 3.x
- JupyterLab
- NumPy
- SciPy
- Matplotlib
- ipywidgets
- pandas only if useful for tabular trade studies
- scikit-learn only if a later notebook genuinely benefits from it

Optional later additions:

- Plotly for interactive visualization
- numba for performance if needed

The initial version should avoid unnecessary framework complexity.

## 13. Pedagogical Quality Requirements

- Explanations must prioritize intuition before abstraction.
- Mathematical notation must be consistent across notebooks.
- Variables and coordinate systems must be clearly defined.
- Important assumptions must be stated explicitly.
- Each notebook must answer: what problem is being solved, why this method works, and when this method fails.
- Tradeoff discussion must be treated as a first-class requirement, not an optional appendix.

## 14. SAS-Specific Learning Outcomes

By the end of the notebook sequence, the learner should be able to:

- Explain why matched filtering improves range resolution and detection performance.
- Explain how array aperture affects angular resolution.
- Explain why phase coherence matters for SAS.
- Describe how platform motion contributes to synthetic aperture formation.
- Explain the difference between an unfocused and focused SAS representation.
- Describe the major stages of a simplified SAS pipeline.
- Identify common tradeoffs involving bandwidth, aperture length, sampling density, sidelobes, and computation.
- Reason about how model errors or hardware limitations can degrade final image quality.

## 15. Deliverables

### Required Deliverables

- `SPEC.md`
- A top-level `README.md` describing the curriculum and setup
- A sequenced set of notebooks under `notebooks/`
- Shared Python helpers under `src/sonar_py_lib/`
- Environment/setup definition

### Optional Deliverables

- Small quizzes or exercises
- A glossary notebook or appendix
- A capstone notebook comparing multiple SAS processing choices
- Exported figures for later reference

## 16. Acceptance Criteria

The first project version is acceptable when:

- A learner can run the notebooks locally in order.
- The notebook sequence forms a coherent conceptual progression.
- Foundational DSP concepts connect clearly to beamforming and then to SAS.
- Each major topic includes simulations and visualizations.
- The final notebooks demonstrate a simplified end-to-end SAS processing pipeline.
- The notebooks explicitly discuss tradeoffs and development decisions, not only formulas.
- A reader can revisit individual notebooks later as a reference without needing to re-derive everything from scratch.

## 17. Risks and Constraints

### Risks

- Too much theory too early can make the curriculum unreadable.
- Too much implementation detail too early can obscure the principles.
- Overly realistic sonar environments can explode scope before core intuition is built.
- Numerical shortcuts can accidentally teach the wrong mental model if not clearly explained.

### Constraints

- The project should remain locally runnable on a normal development machine.
- Notebook runtime should stay reasonable for educational iteration.
- Early notebooks must avoid unnecessary complexity.

## 18. Recommended Development Plan

### Milestone 1: Foundations

- Set up repository structure
- Create shared plotting and DSP utilities
- Implement notebooks 1 through 5

### Milestone 2: Sonar and Ranging

- Implement notebooks 6 through 8
- Create basic scene and echo simulators

### Milestone 3: Arrays and Beamforming

- Implement notebooks 9 through 11
- Build reusable array and beam pattern helpers

### Milestone 4: SAS Core

- Implement notebooks 12 through 15
- Add simple image formation workflow

### Milestone 5: Trade Studies and Refinement

- Implement notebook 16
- Improve explanations, plots, and consistency
- Add exercises and recap material

## 19. Open Design Decisions

These should be resolved during implementation:

- Whether to standardize on `pyproject.toml` or `environment.yml`
- Whether interactive widgets are worth the added notebook complexity
- Whether to include a minimal motion compensation section in the first version
- Whether to implement backprojection first or use a simpler focusing approximation first
- How much underwater acoustics detail to include before it distracts from SAS fundamentals

## 20. Success Definition

This project is successful if the notebook set becomes a dependable reference that helps the learner:

- rebuild core DSP intuition,
- understand beamforming and aperture concepts concretely,
- reason about SAS pipeline design choices,
- and connect mathematical principles to implementation tradeoffs with enough depth to support future experimentation and development.
