# Architecture

The lab is organized as a pipeline. Each stage emits structured records that
can be checked, clustered, and reviewed by another agent.

## 1. Residue Engine

Input:

- Ordered exponent signatures `(p,q,r)` from `{3,4,5,7,11,13}`.
- Odd primes `ell`.

For each `(p,q,r,ell)` the engine computes nonzero power residue sets:

```text
R_p(ell) = { a^p mod ell : a in F_ell^* }
```

It then counts primitive local survivors of

```text
u + v = w mod ell,
u in R_p(ell), v in R_q(ell), w in R_r(ell).
```

The current primitive proxy is "all three local classes are nonzero." Global
coprimality is not inferred from a single prime.

Measured fields include:

- Survivor count and pair density.
- Shannon entropy of the output residue distribution.
- Lift survival to unit power residues modulo `ell^2`.
- Residue fingerprints based on subgroup shape and coarse density/lift buckets.
- Randomized multiplicative subgroup-coset controls with matching cardinalities.

## 2. Valuation Engine

The valuation layer asks whether the residue survivors behave like the start of
a local descent obstruction.

It records:

- Zero-class solution counts after adjoining zero to each residue set.
- Zero-dominance ratios.
- Unit lift failure rates.
- Flags such as `no_unit_lifts`, `high_lift_failure`,
  `zero_class_dominates`, and `descent_like_chain`.

These are diagnostics, not theorems. They are intended to help identify
patterns worth turning into precise lemmas.

## 3. Zero-Support Engine

The zero-support layer converts coarse zero-class dominance into exact masks.
For every zero-adjoined local survivor it records whether the support is:

```text
none, A_only, B_only, C_only, AB, AC, BC, ABC
```

This distinction matters because one-variable divisibility is not a primitive
contradiction. A primitive counterexample may have `ell | A` while
`ell` does not divide `B` or `C`. The promising cases are:

- every local survivor has at least two variables zero modulo `ell`;
- every local survivor has the same exact one-variable mask, and p-adic lifting
  makes that branch impossible or forces valuation growth;
- unit survivors exist but are unusually sparse against controls.

## 4. Primitive Obstruction Classifier

Rows are classified as:

- `direct_primitive_obstruction`
- `mandatory_single_divisor`
- `sparse_unit_survivor`
- `likely_small_prime_artifact`
- `control_like`

Small-prime and trivial subgroup-collapse rows are intentionally demoted so they
do not masquerade as Beal-type contradictions.

## 5. P-Adic Lift Audit

Mandatory single-divisor rows are lifted through `ell^2` and `ell^3` where
feasible. The audit is conservative: for exponents greater than `2`, a variable
divisible exactly once by `ell` already contributes `0` modulo `ell^3`, so no
valuation growth is claimed unless the branch actually dies.

## 6. Unit-Survivor Geometry

Sparse nonzero rows are analyzed more deeply before they are treated as
potential lemma candidates.

For each sparse unit row, the geometry layer records:

- actual survivor triples `(u,v,w)`;
- subgroup sizes and `gcd(e, ell - 1)` shape;
- marginal/coset concentration;
- orbit structure under common multiplicative scaling;
- symmetry under swapping the `A` and `B` variables;
- additive energy of `H_p + H_q`;
- intersection size of `H_p + H_q` with `H_r`;
- survivor entropy and compression.

The artifact explainer demotes rows explained by:

- tiny primes;
- trivial or order-two power images such as `{1,-1}`;
- identical subgroup-size families that reproduce the same sparse behavior.

Character fingerprints record Legendre and higher-character distributions. The
unit lift audit checks whether unit survivor triples persist, expand, or
collapse through `ell^2` and `ell^3`.

Multi-prime compatibility uses CRT-style products honestly: nonempty local unit
constraints remain nonempty under independent CRT products. The module ranks
combined density and rigidity instead of claiming a contradiction.

## 7. Modular Shadow

The modular-shadow router is the follow-up stage for sparse unit rows that are
not already explained as subgroup artifacts. It does not claim local
contradictions. It ranks proof-route sketches that would need a separate
Frey-curve, conductor, irreducibility, or newform argument.

The router currently targets:

```text
(4,7,7), (7,4,7), (5,4,5), (4,5,5),
(3,5,5), (5,3,5), (7,7,4), (3,4,3)
```

The stage is split into small records:

- `signature_normalizer.py` canonicalizes signatures up to swapping `A/B` and
  records repeated exponents, fourth-power involvement, and mixed-prime shape.
- `frey_template_library.py` records symbolic Frey-style templates such as
  `E: y^2 = x(x - A^p)(x + B^q)`, together with discriminant support,
  bad-prime support, confidence, and uncertainty flags.
- `finite_field_trace_probe.py` instantiates nonsingular candidate curves over
  `F_ell`, counts points, computes `a_ell`, and compares trace distributions
  against same-size subgroup controls.
- `cross_prime_trace_compatibility.py` groups trace fingerprints by canonical
  signature and labels repeated patterns as `trace_rigid`,
  `trace_control_like`, `trace_artifact`, or `needs_newform_check`.
- `sage_optional_newform_probe.py` runs only when SageMath is available. If
  Sage is missing, it writes skip rows and instructions.
- `modular_route_classifier.py` labels rows as proof-route sketches, artifact
  explained rows, or follow-up candidates.

Promotion is stricter than local sparsity. A row is not promoted because its
unit survivor density is low. It must survive artifact checks, have reasonable
template confidence, and show trace behavior that separates from structured
same-size controls.

## 8. Known-Case Calibration

The known-case calibration harness turns the scanner into a route recognizer.
It runs the existing RSG layers over a JSON-backed library of generalized
Fermat calibration cases and compares expected proof shape with actual system
labels.

The bundled library includes:

- diagonal `(p,p,p)` Fermat-style cases;
- repeated-exponent `(p,p,q)` cases;
- fourth-power bridges `(4,p,p)`, `(p,4,p)`, and `(p,p,4)`;
- mixed cases such as `(3,4,3)`, `(3,5,5)`, `(4,7,7)`,
  `(5,4,5)`, and `(7,7,4)`;
- artifact calibrators such as previous order-two subgroup rows.

Each case stores a signature, family label, known status, expected route,
notes, and a citation placeholder. The file is a calibration harness, not a
complete theorem database.

The calibration runner produces:

- expected-vs-actual labels: `calibrated_route_candidate`, `artifact_like`,
  `known_case_mismatch`, `needs_external_sage_check`, or
  `not_promising_yet`;
- theorem-terrain route labels such as `diagonal_flt_style`,
  `known_modular_method_shape`, `fourth_power_bridge`,
  `local_obstruction_shape`, and `artifact_prone_shape`;
- route confusion buckets for false positives, false negatives, artifact
  matches, and modular-method routing;
- a theorem-terrain-aware route matrix with
  `correct_artifact_demotion`, `correct_theorem_terrain_route`,
  `correct_external_sage_route`, `route_unknown`, `true_mismatch`, and
  `overpromoted_candidate`;
- route-collision triage that separates `local_artifact_evidence`,
  `signature_terrain_evidence`, `modular_route_evidence`,
  `unit_geometry_evidence`, and `padic_lift_evidence`;
- structured family-expansion rows that test whether nearby signatures preserve
  or break residue fingerprints;
- route-prior scores with artifact likelihood and discovery readiness;
- optional `.sage` scripts for finite-field trace checks and later newform
  placeholders.
- Sage/newform follow-up jobs with machine-readable JSON imports, conservative
  route-confidence updates, and known-case safety checks.

Promotion discipline is strict: a Beal candidate should not move into discovery
mode unless the same route type behaves correctly on calibration cases and does
not match known artifact behavior.

The theorem-terrain classifier runs after artifact/local/lift checks and before
modular-shadow promotion. Diagonal FLT-style cases are routed to known theorem
terrain instead of being treated as failures of local RSG methods.

The route-collision resolver runs at signature level. A single artifact-prone
local prime can force caution, but it cannot globally demote a known
modular-method signature unless artifact evidence dominates the signature. The
only conservative resolutions are external Sage/newform checks, theorem-terrain
routes, artifact demotion, or continued blocking; never proof promotion.

## 9. Sage/Newform Follow-Up

The Sage follow-up loop starts where route collision leaves off. It collects
signatures labeled `needs_external_sage_check`, `mixed_needs_external_check`,
`newform_check_candidate`, or `trace_rigid_candidate` and writes:

- one `.sage` job per signature;
- a combined `run_all_sage_jobs.sage` batch file;
- a `sage_job_manifest.csv` metadata table;
- a `sage_results/` directory for JSON outputs.

Each job includes the signature, route label, source run, candidate rows, primes
involved, symbolic Frey template, heuristic conductor-like levels, and explicit
limitations. The generated Sage code computes finite-field trace rows and small
newform counts where supported, then writes JSON.

`sage_environment_detector.py` detects native Sage, WSL Sage, Docker, CI mode,
or unavailable execution. `sage_docker_runner.py` builds container commands
using `SAGE_DOCKER_IMAGE` when provided. `sage_followup_cli.py` exposes the
roundtrip as `detect`, `generate`, `run`, `import`, `summarize`, and
`roundtrip`.

`sage_smoke.py` writes a deterministic Sage smoke job before the real queue.
`sage_job_runner.py` executes smoke and real jobs with per-job timeout handling.
When Sage times out or fails before writing output, the runner writes
importer-compatible JSON with `sage_status` set to `timeout` or `failed`.

`sage_result_importer.py` validates Sage JSON and rejects any row that attempts
to allow contradiction claims. `modular_confidence_updater.py` can move a row
only to conservative labels such as `needs_external_sage_check`,
`sage_checked_inconclusive`, `modular_followup_candidate`, `artifact_like`, or
`not_promising_yet`. In roundtrip reports, the highest human-facing review label
is `worth_human_modular_review`. `known_case_sage_calibration.py` verifies that
artifacts remain demoted and known theorem/modular terrain does not become
overpromoted.

`candidate_dossier_generator.py` writes one markdown dossier per queued
signature. Each dossier records terrain, artifact risk, sparse rows, p-adic
status, Frey-template confidence, Sage status, the gap to a theorem claim, and
the recommended next mathematical check.

If SageMath is unavailable, the default run still passes. Jobs are generated,
imports are marked `unavailable`, and the route remains queued for external
Sage/newform review.

## 10. Experiment Runner

The runner writes each sweep to `runs/<timestamp>/`:

- `summary.csv`: one row per `(p,q,r,ell)`.
- `interesting_cases.csv`: ranked candidate/watchlist rows.
- `clusters.csv`: repeated obstruction fingerprints.
- `zero_support_summary.csv`: exact zero-support and primitive classification.
- `direct_obstructions.csv`: exact direct primitive obstruction candidates.
- `mandatory_single_divisor_candidates.csv`: exact one-variable candidates with
  p-adic audit fields.
- `sparse_unit_clusters.csv`: larger-prime sparse unit-survivor clusters.
- `unit_survivor_summary.csv`: sparse-row geometry, artifact, character, and
  unit-lift data.
- `artifact_demotions.csv`: rows explained by subgroup artifacts.
- `unexplained_sparse_rows.csv`: rows that need modular-shadow follow-up.
- `padic_unit_lift_results.csv`: `ell^2`/`ell^3` unit-lift behavior.
- `multi_prime_cluster_results.csv`: CRT-style combined-density records.
- `modular_shadow_summary.csv`: joined route, classifier, template, and trace
  data for target signatures.
- `frey_template_candidates.csv`: symbolic Frey-template records.
- `trace_probe_results.csv`: finite-field trace fingerprints.
- `cross_prime_trace_results.csv`: canonical trace compatibility records.
- `newform_probe_results.csv`: Sage availability or optional newform-check
  instructions.
- `known_case_calibration_summary.csv`: known-case expected-vs-actual route
  comparison.
- `route_confusion_matrix.csv`: calibration confusion buckets.
- `theorem_terrain_summary.csv`: structural theorem-terrain route rows.
- `known_case_route_matrix.csv`: theorem-terrain-aware calibration buckets.
- `remaining_true_mismatches.csv`: true mismatch and overpromotion rows.
- `route_collision_summary.csv`: signature-level collision evidence.
- `resolved_known_mismatches.csv`: collisions resolved to external/theorem
  routes.
- `still_blocked_mismatches.csv`: collisions still blocking promotion.
- `family_expansion_results.csv`: nearby-signature fingerprint comparisons.
- `route_prior_scores.csv`: calibrated route-priority scores.
- `sage_export_manifest.csv`: optional Sage script manifest.
- `sage_job_manifest.csv`: generated Sage/newform job metadata.
- `sage_environment.json`: machine-readable execution-mode detection.
- `sage_environment_report.md`: human-readable Sage environment report.
- `sage_execution_manifest.csv`: native, WSL, Docker, or CI command hints.
- `sage_import_results.csv`: validated Sage JSON imports or skip rows.
- `sage_known_case_calibration.csv`: known-case safety after Sage import.
- `modular_confidence_summary.csv`: conservative post-Sage route confidence.
- `sage_roundtrip_summary.csv`: import and human-review label per job.
- `candidate_dossier_manifest.csv`: generated dossier paths and labels.
- `candidate_dossier_index.md`: run-local dossier index.
- `metadata.json`: parameters and reproducibility data.
- `README_REPORT.md`: human-readable report.
- `README_ZERO_SUPPORT_REPORT.md`: exact zero-support report.
- `README_UNIT_GEOMETRY_REPORT.md`: sparse unit-geometry report.
- `README_MODULAR_SHADOW_REPORT.md`: proof-route sketch report.
- `README_KNOWN_CASE_CALIBRATION_REPORT.md`: known-case calibration report.
- `README_THEOREM_TERRAIN_REPORT.md`: theorem-terrain calibration report.
- `README_ROUTE_COLLISION_REPORT.md`: route-collision triage report.
- `README_SAGE_FOLLOWUP_REPORT.md`: Sage/newform follow-up report.

The generated report explicitly avoids proof language.
