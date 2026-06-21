# Beal RSG Lab

`beal_rsg_lab` is a computational research lab for finding reusable obstruction
patterns in primitive generalized Fermat equations

```text
A^x + B^y = C^z,  x,y,z > 2,  gcd(A,B,C) = 1.
```

The Beal Conjecture is the flagship test case, but the code does not try to
prove Beal directly. It searches for residue, valuation, and modular-shadow
patterns that primitive counterexamples would be forced to satisfy.

## Current Engine

- `beal_rsg_lab/rsg_residue_engine.py`: residue sets, survivor density, entropy,
  lift survival to `ell^2`, repeated fingerprints, and randomized coset controls.
- `beal_rsg_lab/rsg_valuation_engine.py`: zero-class, lift-failure, and
  descent-like valuation diagnostics.
- `beal_rsg_lab/zero_support_engine.py`: exact zero-support masks
  (`none`, `A_only`, `B_only`, `C_only`, `AB`, `AC`, `BC`, `ABC`) for
  zero-adjoined local survivors.
- `beal_rsg_lab/primitive_obstruction_classifier.py`: separates direct
  primitive obstructions, mandatory single-divisor candidates, sparse unit
  survivors, and likely small-prime artifacts.
- `beal_rsg_lab/padic_lift_audit.py`: conservative `ell^2`/`ell^3` audit for
  mandatory single-divisor rows.
- `beal_rsg_lab/exact_explanation_generator.py`: human-readable modular
  explanations for top rows.
- `beal_rsg_lab/unit_survivor_geometry.py`: geometry metrics for sparse nonzero
  unit survivors, including triples, orbits, additive energy, entropy, and
  compression.
- `beal_rsg_lab/artifact_explainer.py`: demotes sparse rows explained by tiny
  power images, order-two images, or identical subgroup-size controls.
- `beal_rsg_lab/character_fingerprint.py`: Legendre and higher-character
  fingerprints for survivor triples.
- `beal_rsg_lab/padic_unit_lift.py`: `ell^2`/`ell^3` unit-survivor lift audit.
- `beal_rsg_lab/multi_prime_compatibility.py`: CRT-style combined-density
  compatibility for repeated sparse signatures.
- `beal_rsg_lab/exact_sparse_lemma_generator.py`: human-readable sparse
  unit-survivor lemma explanations.
- `beal_rsg_lab/rsg_modular_shadow.py`: symbolic obstruction records,
  conductor-like complexity, Frey-curve placeholder data, and candidate ranking.
- `beal_rsg_lab/signature_normalizer.py`: canonical signature IDs under
  `A/B` swapping, with repeated-exponent and fourth-power flags.
- `beal_rsg_lab/frey_template_library.py`: symbolic Frey-style template records
  with uncertainty flags rather than proof claims.
- `beal_rsg_lab/frey_reduction_diagnostics_545.py`: focused
  q in `{3,13,17,41,61}` invariant-valuation diagnostics for the `(5,4,5)`
  single masks.
- `beal_rsg_lab/tate_algorithm_stub_545.py`: safe symbolic Tate-algorithm
  stub that downgrades missing invariant formulas to human review.
- `beal_rsg_lab/single_mask_newform_pressure_545.py`: combines unit trace
  results, newform coefficients, and focused reduction labels for `A_only`,
  `B_only`, and `C_only`.
- `beal_rsg_lab/multiplicative_reduction_congruence_545.py`: audits
  `A_only`, `B_only`, and `C_only` against the conditional
  `a_q(f) == +/-(q+1) mod 5` multiplicative-reduction congruence at
  q in `{3,13,17,41,61}`.
- `beal_rsg_lab/local_case_closure_score_545.py`: combines unit traces,
  primitive-forbidden pairwise masks, and multiplicative congruence rows into
  conservative q-level local-closure labels.
- `beal_rsg_lab/best_eliminating_prime_545.py`: ranks the focused eliminating
  good primes by unit survivors, single-mask survivors, congruence coverage,
  q=3 reliance, and human-review priority.
- `beal_rsg_lab/cross_prime_branch_compatibility_545.py`: checks whether the
  non-q=3 focused primes jointly remove all compatible unit and single-mask
  branch assignments for each level-220 newform.
- `beal_rsg_lab/q3_exceptionality_audit_545.py`: records why q=3 is a good
  prime for level 220 and whether its behavior is supported by the larger
  focused primes.
- `beal_rsg_lab/best_route_summary_545.py`: ranks q=3 single-prime closure,
  non-q=3 cross-prime closure, partial closures, and survivor routes.
- `beal_rsg_lab/quantifier_safety_audit_545.py`: verifies the
  exists-prime-per-newform quantifier for the non-q=3 cross-prime route.
- `beal_rsg_lab/conditional_theorem_packet_545.py`: writes the conditional
  theorem-review packet for the focused `(5,4,5)` route.
- `beal_rsg_lab/assumption_dependency_graph_545.py`: records the dependency
  chain from Frey attachment through quantifier safety.
- `beal_rsg_lab/adversarial_review_checklist_545.py`: writes the human review
  checklist for level, reduction, coefficient-field, and branch-coupling risks.
- `beal_rsg_lab/frey_curve_derivation_545.py`: computes symbolic c4, c6,
  discriminant, and j-invariant formulas for the proposed `(5,4,5)` Frey
  object.
- `beal_rsg_lab/conductor_support_audit_545.py`: audits the expected bad-prime
  support behind candidate level 220.
- `beal_rsg_lab/conductor_exponent_model_545.py`: records symbolic valuation
  and conductor-exponent expectations for ABC primes and bad primes 2, 5, 11.
- `beal_rsg_lab/level_220_provenance_545.py`: explains the current provenance
  of `220 = 2^2 * 5 * 11` and flags `level_11_factor_unjustified`.
- `beal_rsg_lab/abc_prime_removal_audit_545.py`: tracks the level-lowering
  gap for removing primes dividing A, B, or C from the comparison level.
- `beal_rsg_lab/sage_conductor_sanity_samples_545.py`: generates an optional
  Sage sanity script for invariant formulas and synthetic local samples.
- `beal_rsg_lab/bad_prime_tate_checklist_545.py`: lists local Tate-algorithm
  checks at bad primes 2, 5, and 11.
- `beal_rsg_lab/level_lowering_obligation_545.py`: records the formal
  residual, modularity, level-lowering, target-level, and trace-validity
  obligations.
- `beal_rsg_lab/conditional_route_validity_score_545.py`: conservatively scores
  the quantifier-safe route against the Frey/conductor/level-lowering gaps.
- `beal_rsg_lab/finite_field_trace_probe.py`: point-count and trace probes for
  nonsingular candidate Frey curves over finite fields.
- `beal_rsg_lab/modular_shadow_engine.py`: route scoring that combines
  non-artifact survivor geometry, Frey templates, and trace rigidity.
- `beal_rsg_lab/cross_prime_trace_compatibility.py`: canonical-signature trace
  compatibility across repeated prime shadows.
- `beal_rsg_lab/sage_optional_newform_probe.py`: optional Sage availability and
  newform-check instructions.
- `beal_rsg_lab/modular_route_classifier.py`: final proof-route sketch
  classification.
- `beal_rsg_lab/known_case_library.py`: JSON-backed generalized Fermat
  calibration cases.
- `beal_rsg_lab/calibration_runner.py`: known-case route calibration harness.
- `beal_rsg_lab/route_confusion_matrix.py`: expected-vs-actual route buckets.
- `beal_rsg_lab/signature_family_expander.py`: structured family expansion
  around known signatures.
- `beal_rsg_lab/route_prior_model.py`: calibrated proof-route and artifact
  scoring.
- `beal_rsg_lab/sage_export_scripts.py`: optional Sage scripts for modular
  follow-up cases.
- `beal_rsg_lab/sage_job_generator.py`: per-signature Sage/newform job files
  with JSON-output metadata.
- `beal_rsg_lab/sage_result_importer.py`: Sage JSON schema validation and
  conservative result import.
- `beal_rsg_lab/sage_environment_detector.py`: native Sage, WSL Sage, Docker,
  and CI execution-mode detection.
- `beal_rsg_lab/sage_docker_runner.py`: Docker command construction for Sage
  batch execution.
- `beal_rsg_lab/sage_roundtrip.py`: execution and import summary row builders.
- `beal_rsg_lab/sage_followup_cli.py`: `detect`, `generate`, `import`, and
  `summarize` commands for Sage roundtrips.
- `beal_rsg_lab/sage_smoke.py`: deterministic Sage smoke job generation.
- `beal_rsg_lab/sage_job_runner.py`: timeout-aware native, WSL, and Docker
  Sage execution.
- `beal_rsg_lab/candidate_dossier_generator.py`: markdown dossiers for queued
  modular-route signatures.
- `beal_rsg_lab/modular_confidence_updater.py`: post-Sage route-confidence
  updates capped at human-review candidates.
- `beal_rsg_lab/known_case_sage_calibration.py`: known-case safety checks after
  Sage result import.
- `beal_rsg_lab/theorem_terrain_classifier.py`: structural theorem-terrain
  routing for diagonal FLT-style, descent, modular, local, and artifact terrain.
- `beal_rsg_lab/calibration_confusion_matrix.py`: theorem-terrain-aware route
  matrix.
- `beal_rsg_lab/terrain_report_generator.py`: terrain summary and mismatch
  reports.
- `beal_rsg_lab/route_collision_resolver.py`: signature-level triage that
  separates local artifact primes from global theorem/modular terrain.
- `beal_rsg_lab/run_experiment.py`: full sweep runner that writes
  the broad RSG files plus zero-support, unit-geometry, modular-shadow, and
  theorem-terrain calibration reports under `runs/<timestamp>/`.

## Quick Start

```powershell
python -m unittest discover
python run_experiment.py --prime-limit 31 --control-samples 16
python -m beal_rsg_lab.sage_followup_cli detect
python -m beal_rsg_lab.sage_followup_cli import --run-dir runs/<run-id>
python -m beal_rsg_lab.sage_followup_cli summarize --run-dir runs/<run-id>
python -m beal_rsg_lab.sage_followup_cli roundtrip --run-dir runs/<run-id> --skip-generate --backend docker
```

For a faster smoke run:

```powershell
python run_experiment.py --primes 5,7,11 --control-samples 6 --no-lift
```

## Research Standard

The report ranks possible publishable obstruction candidates. It must not be
read as a proof. A pattern is promoted only when it repeats across multiple
prime/signature contexts, beats randomized subgroup-coset controls, and passes
known-case calibration without matching artifact behavior.

See:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md)
- [docs/RESEARCH_STATUS.md](docs/RESEARCH_STATUS.md)
- [docs/reports/initial_20260620_103500.md](docs/reports/initial_20260620_103500.md)
- [docs/reports/zero_support_20260620_105000.md](docs/reports/zero_support_20260620_105000.md)
- [docs/reports/unit_geometry_20260620_111500.md](docs/reports/unit_geometry_20260620_111500.md)
- [docs/reports/modular_shadow_20260620_154000.md](docs/reports/modular_shadow_20260620_154000.md)
- [docs/reports/known_case_calibration_20260620_163000.md](docs/reports/known_case_calibration_20260620_163000.md)
- [docs/reports/theorem_terrain_20260620_174500.md](docs/reports/theorem_terrain_20260620_174500.md)
- [docs/reports/route_collision_20260620_181500.md](docs/reports/route_collision_20260620_181500.md)
- [docs/reports/sage_followup_20260620_183000.md](docs/reports/sage_followup_20260620_183000.md)
- [docs/SAGE_FOLLOWUP.md](docs/SAGE_FOLLOWUP.md)
- [docs/dossiers/candidate_dossier_index.md](docs/dossiers/candidate_dossier_index.md)
- [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)
