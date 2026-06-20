# Agent Guide

This repository should stay useful to future agents. Keep claims modest, keep
outputs structured, and make each experiment reproducible.

## Important Commands

```powershell
python -m unittest discover
python run_experiment.py --prime-limit 31 --control-samples 16
python run_experiment.py --primes 5,7,11 --control-samples 6 --no-lift
python -m beal_rsg_lab.sage_followup_cli detect --run-dir runs\<run-id>
python -m beal_rsg_lab.sage_followup_cli import --run-dir runs\<run-id>
python -m beal_rsg_lab.sage_followup_cli summarize --run-dir runs\<run-id>
```

## Source Map

- `beal_rsg_lab/number_theory.py`: small pure-Python number theory helpers.
- `beal_rsg_lab/rsg_residue_engine.py`: core residue and control computations.
- `beal_rsg_lab/rsg_valuation_engine.py`: valuation-style diagnostics.
- `beal_rsg_lab/zero_support_engine.py`: exact zero-support masks.
- `beal_rsg_lab/primitive_obstruction_classifier.py`: primitive obstruction
  classification and structured subgroup-size controls.
- `beal_rsg_lab/padic_lift_audit.py`: conservative lift audit for mandatory
  single-divisor candidates.
- `beal_rsg_lab/exact_explanation_generator.py`: modular explanation text.
- `beal_rsg_lab/unit_survivor_geometry.py`: survivor triples and unit-geometry
  metrics.
- `beal_rsg_lab/artifact_explainer.py`: subgroup-artifact demotion logic.
- `beal_rsg_lab/character_fingerprint.py`: multiplicative-character summaries.
- `beal_rsg_lab/padic_unit_lift.py`: sparse unit lift audit through `ell^3`.
- `beal_rsg_lab/multi_prime_compatibility.py`: combined-density CRT checks.
- `beal_rsg_lab/exact_sparse_lemma_generator.py`: sparse lemma explanation text.
- `beal_rsg_lab/rsg_modular_shadow.py`: symbolic obstruction and clustering.
- `beal_rsg_lab/signature_normalizer.py`: canonical modular-route signatures.
- `beal_rsg_lab/frey_template_library.py`: symbolic Frey-style template records.
- `beal_rsg_lab/finite_field_trace_probe.py`: finite-field point counts and
  trace distributions for nonsingular candidate Frey curves.
- `beal_rsg_lab/modular_shadow_engine.py`: modular route scoring.
- `beal_rsg_lab/cross_prime_trace_compatibility.py`: repeated trace
  fingerprints across primes.
- `beal_rsg_lab/sage_optional_newform_probe.py`: optional Sage newform probe
  hooks and skip instructions.
- `beal_rsg_lab/modular_route_classifier.py`: proof-route sketch labels.
- `beal_rsg_lab/known_case_library.py`: JSON-backed calibration cases.
- `beal_rsg_lab/calibration_runner.py`: known-case calibration orchestration.
- `beal_rsg_lab/route_confusion_matrix.py`: known-vs-system route buckets.
- `beal_rsg_lab/signature_family_expander.py`: structured nearby-signature
  expansion around known families.
- `beal_rsg_lab/route_prior_model.py`: calibrated route-priority scoring.
- `beal_rsg_lab/sage_export_scripts.py`: optional `.sage` script generation.
- `beal_rsg_lab/sage_job_generator.py`: external Sage/newform job generation.
- `beal_rsg_lab/sage_environment_detector.py`: native, WSL, Docker, and CI
  execution detection.
- `beal_rsg_lab/sage_docker_runner.py`: Docker command construction.
- `beal_rsg_lab/sage_followup_cli.py`: Sage roundtrip CLI.
- `beal_rsg_lab/sage_result_importer.py`: Sage JSON schema validation and
  import.
- `beal_rsg_lab/candidate_dossier_generator.py`: queued-signature dossier
  generation.
- `beal_rsg_lab/modular_confidence_updater.py`: conservative post-Sage route
  confidence updates.
- `beal_rsg_lab/known_case_sage_calibration.py`: known-case safety checks after
  Sage import.
- `beal_rsg_lab/theorem_terrain_classifier.py`: structural theorem-terrain
  routing.
- `beal_rsg_lab/calibration_confusion_matrix.py`: terrain-aware route matrix.
- `beal_rsg_lab/terrain_report_generator.py`: theorem-terrain reports.
- `beal_rsg_lab/route_collision_resolver.py`: signature-level artifact/terrain
  collision triage.
- `beal_rsg_lab/run_experiment.py`: orchestration and file outputs.
- `tests/`: deterministic unit and smoke tests.

The full unit-geometry sweep with `--prime-limit 31 --control-samples 16` can
take several minutes because it enumerates unit lifts through `ell^3` for sparse
rows.

The modular-shadow outputs should be read as route triage only. Trace-rigid
rows may become proof-route candidates; `needs_newform_check` rows are logged
for later Sage or modular-form work and do not count as contradictions.

Known-case calibration is now part of the default run. Treat
`known_case_mismatch` rows as calibration debt and `artifact_like` rows as
controls. Do not promote a new Beal candidate until the same route type behaves
correctly on the calibration library.

Theorem-terrain routing is also part of the default run. Diagonal FLT-style
cases should route to `theorem_terrain_route`; this is a calibration success,
not a new proof. `true_mismatch` and `overpromoted_candidate` rows block
discovery-mode promotion until explained.

Route-collision triage is the final calibration pass. A known modular signature
with one artifact-prone local prime may resolve to `needs_external_sage_check`,
but never to a proof route. True subgroup artifacts should remain
`artifact_like`.

Sage follow-up is now a generated-job and JSON-import loop. If Sage is not on
PATH, the default run still succeeds and marks the imports `unavailable`.
Imported Sage rows must keep `contradiction_claim_allowed` false, and the
strongest post-import label is `modular_followup_candidate`, meaning human
review is worthwhile.

Before handing Sage candidates to a human, generate dossiers with
`python -m beal_rsg_lab.sage_followup_cli summarize`. Committed dossiers live in
`docs/dossiers/`; run-local dossier indexes live in `runs/<run-id>/`.

## Documentation Rules

- Keep `README.md` short.
- Put mathematical protocol in `docs/EXPERIMENT_PROTOCOL.md`.
- Put implementation structure in `docs/ARCHITECTURE.md`.
- Generated reports live under `runs/` and are ignored by Git unless a specific
  run is intentionally promoted into documentation.

## Research Safety

Never state that the engine proves Beal. The strongest appropriate wording is
"publishable obstruction candidate" or "lemma candidate." Every promoted
candidate must pass the repeat and randomized-control gates.
