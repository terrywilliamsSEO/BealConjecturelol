# Research Status

## Initial Sweep

Run folder:

```text
runs/initial_20260620_103500
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp initial_20260620_103500
```

Scope:

- Exponent signatures: all ordered triples from `{3,4,5,7,11,13}`.
- Odd primes: `3, 5, 7, 11, 13, 17, 19, 23, 29, 31`.
- Rows: `2160`.
- Lift survival: enabled.
- Randomized subgroup-coset controls: `16` samples per row.

Output summary:

- Promoted candidates: `54`.
- Watchlist rows: `619`.
- Generated files: `summary.csv`, `interesting_cases.csv`, `clusters.csv`,
  `metadata.json`, and `README_REPORT.md`.
- Committed report: [reports/initial_20260620_103500.md](reports/initial_20260620_103500.md).

## Current Leading Pattern

The strongest early rows are local-empty or very sparse residue patterns tied
to signatures with repeated fourth-power structure at small primes, especially
`ell = 5`, plus broader repeated clusters at larger primes.

This is not evidence of a proof. It is a queue of obstruction candidates. The
next serious step is to restate the strongest clusters as exact local lemmas and
then test them against a wider prime range and stricter lift/modular-shadow
consistency checks.

## Zero-Support Upgrade

Run folder:

```text
runs/zero_support_20260620_105000
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp zero_support_20260620_105000
```

Output summary:

- Rows: `2160`.
- Direct primitive obstructions: `0`.
- Mandatory single-divisor candidates: `0`.
- Sparse unit-survivor rows: `105`.
- Likely small-prime artifacts: `640`.
- Control-like rows: `1415`.
- Sparse unit clusters: `53`.
- Committed report: [reports/zero_support_20260620_105000.md](reports/zero_support_20260620_105000.md).

Interpretation:

The stricter pass demotes the earlier `ell = 5` fourth-power rows. They are real
local subgroup-collapse phenomena, but not primitive contradictions. The active
research track is now larger-prime sparse unit-survivor clusters such as
`4-11-11` at `ell = 23`, `4-7-7` at `ell = 29`, and `7-7-4` at `ell = 29`.

## Unit-Geometry Upgrade

Run folder:

```text
runs/unit_geometry_20260620_111500
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp unit_geometry_20260620_111500
```

Output summary:

- Sparse unit rows analyzed: `105`.
- Artifact explained rows: `85`.
- Unexplained sparse rows: `20`.
- Collapse or rigid unit-lift rows: `0`.
- Multi-prime compatibility records: `1`.
- Committed report: [reports/unit_geometry_20260620_111500.md](reports/unit_geometry_20260620_111500.md).

Interpretation:

Most previously interesting sparse rows are explained by order-two power images
or identical subgroup-size families. In particular, the `ell = 23` rows with
11th powers are now demoted because the 11th-power image is `{1,-1}`. The
remaining 20 rows need modular-shadow follow-up, but none collapse or become
rigid under the current `ell^2`/`ell^3` unit-lift audit.

## Modular-Shadow Router

Run folder:

```text
runs/modular_shadow_20260620_154000
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp modular_shadow_20260620_154000
```

Output summary:

- Target sparse rows routed: `17`.
- Artifact explained route rows: `6`.
- Proof-route candidate rows: `0`.
- Trace-rigid candidate rows: `0`.
- Newform-check sketch rows: `4`.
- Sage available: `False`.
- Committed report: [reports/modular_shadow_20260620_154000.md](reports/modular_shadow_20260620_154000.md).

Interpretation:

The router found no Beal obstruction and no promoted proof-route candidate.
Every target trace distribution matched the same-size subgroup trace support in
the current finite-field probe. The repeated canonical signature `3-4-3`
appears across `ell = 13, 19, 31` and is therefore logged as a
`needs_newform_check` sketch, but it is not trace-rigid and not promoted.

The `ell = 29` and `ell = 31` fourth-power bridge rows remain Frey-template
follow-up sketches. They have reasonable symbolic template confidence, but the
trace probes do not separate from structured controls.

## Known-Case Calibration Harness

Run folder:

```text
runs/known_case_calibration_20260620_163000
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp known_case_calibration_20260620_163000
```

Output summary:

- Known/calibration cases: `19`.
- `known_case_mismatch`: `6`.
- `artifact_like`: `2`.
- `needs_external_sage_check`: `10`.
- `calibrated_route_candidate`: `0`.
- Sage available: `False`.
- Sage scripts exported: `11`.
- Committed report: [reports/known_case_calibration_20260620_163000.md](reports/known_case_calibration_20260620_163000.md).

Interpretation:

The calibration pass is doing useful triage. It correctly demotes the two
order-two subgroup artifact calibrators and routes ten modular-method-style
cases to external Sage follow-up instead of proof claims. It also exposes
calibration debt: the current RSG layers do not recognize diagonal FLT-style
impossibility, so `(3,3,3)`, `(4,4,4)`, `(5,5,5)`, and `(7,7,7)` are marked
`known_case_mismatch`.

No row reached `calibrated_route_candidate`. Discovery mode should stay gated
until the engine can either recognize FLT/descent terrain or explicitly route
those cases to a separate known-proof recognizer.

This specific FLT-terrain gap is addressed by the theorem-terrain layer below.

## Theorem-Terrain Calibration Layer

Run folder:

```text
runs/theorem_terrain_20260620_174500
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp theorem_terrain_20260620_174500
```

Output summary:

- Known/calibration cases: `19`.
- `theorem_terrain_route`: `5`.
- `needs_external_sage_check`: `9`.
- `artifact_like`: `2`.
- `known_case_mismatch`: `3`.
- `calibrated_route_candidate`: `0`.
- Remaining true mismatches: `3`.
- Committed report: [reports/theorem_terrain_20260620_174500.md](reports/theorem_terrain_20260620_174500.md).

Interpretation:

The theorem-terrain layer fixes the earlier FLT calibration problem. Diagonal
FLT-style signatures `(3,3,3)`, `(4,4,4)`, `(5,5,5)`, and `(7,7,7)` now route
to `theorem_terrain_route` instead of `known_case_mismatch`. The descent-style
bridge `(4,3,3)` also routes as theorem terrain.

The modular-method terrain cases mostly remain external-check only. The current
true mismatches are `(5,5,7)`, `(5,3,5)`, and `(5,4,5)`, where the strongest
observed signal is artifact-like sparse-unit behavior at `ell = 11` despite a
modular-method expected route. These should block promotion until a stronger
non-artifact route is found or the calibration library is refined.

## Route-Collision Triage

Run folder:

```text
runs/route_collision_20260620_181500
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp route_collision_20260620_181500
```

Output summary:

- Known/calibration cases: `19`.
- `theorem_terrain_route`: `5`.
- `needs_external_sage_check`: `12`.
- `artifact_like`: `2`.
- `known_case_mismatch`: `0`.
- `calibrated_route_candidate`: `0`.
- Resolved known mismatches: `5`.
- Still blocked mismatches: `0`.
- Committed report: [reports/route_collision_20260620_181500.md](reports/route_collision_20260620_181500.md).

Interpretation:

The route-collision resolver separates local artifact rows from global
signature terrain. The three previous known-case mismatches `(5,5,7)`,
`(5,3,5)`, and `(5,4,5)` no longer get globally demoted by the artifact-prone
`ell = 11` row. They resolve conservatively to `needs_external_sage_check`, not
to proof promotion.

Two adjacent fourth-power bridge rows, `(4,5,5)` and `(5,5,4)`, show the same
artifact-collision pattern and also resolve to external Sage checks. The true
subgroup artifacts `(11,11,13)` and `(11,11,5)` remain correctly demoted as
`artifact_like`.

## Sage/Newform Follow-Up Loop

Run folder:

```text
runs/sage_followup_20260620_183000
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp sage_followup_20260620_183000
```

Output summary:

- Known/calibration cases: `19`.
- Known-case mismatches: `0`.
- Known-case external Sage routes: `12`.
- Sage jobs generated: `13`.
- Sage import rows: `13`.
- Sage import `completed`: `0`.
- Sage import `unavailable`: `13`.
- Sage execution mode: `unavailable`.
- Sage execution manifest rows: `13`.
- Candidate dossiers generated: `13`.
- Known-case overpromotion rows after Sage import: `0`.
- Post-Sage `modular_followup_candidate`: `0`.
- Committed report: [reports/sage_followup_20260620_183000.md](reports/sage_followup_20260620_183000.md).

Interpretation:

The Sage follow-up layer turns external-check routes into executable jobs,
machine-readable JSON imports, environment reports, execution manifests, and
candidate dossiers. Since SageMath was not available locally, native Sage was
missing, WSL launch timed out after 5 seconds, and Docker was not found on PATH.
The roundtrip command wrote an unavailable smoke JSON result and every real-job
import row stayed `unavailable`. This preserves the conservative route label
`needs_external_sage_check` and prevents missing external data from becoming
route confidence.

The generated queue contains 13 signatures, including the route-collision
signatures `(5,5,7)`, `(5,3,5)`, and `(5,4,5)`, plus the repeated
newform-check candidates `(3,4,3)` and `(4,3,3)`. Known artifacts remain
demoted and no known case is overpromoted after Sage import.

The committed dossier index is
[dossiers/candidate_dossier_index.md](dossiers/candidate_dossier_index.md).
The Docker runners and GitHub Actions workflow are now the preferred execution
paths when local Sage is absent.

## Focused `(5,4,5)` Frey Reduction And Closure Audit

Follow-up work now adds a focused diagnostic layer for
`A^5 + B^4 = C^5` at q in `{3,13,17,41,61}`. The earlier q=13 and q=17
checks did not close the local case gap: q=13 left a single-mask
multiplicative branch, while q=17 left a unit-branch survivor. Pairwise masks
remain primitive-forbidden. The single masks `A_only`, `B_only`, and `C_only`
are locally possible, so they are handled separately by
`frey_reduction_diagnostics_545.csv`, `tate_algorithm_stub_545.csv`, and
`single_mask_newform_pressure_545.csv`.

For the current displayed Frey template, the available invariant valuations
classify the focused single masks as `multiplicative_reduction_condition`.
The follow-up congruence audit checks the conditional
`a_q(f) == +/-(q+1) mod 5` multiplicative-reduction test at all five focused
primes. The closure score now records unit-branch survivors, single-mask
survivors, coefficient/formula gaps, and level-lowering assumptions for each
q. `best_eliminating_prime_545.csv` and `BEST_ELIMINATING_PRIME_545.md` rank
the focused primes by fewest surviving branches, cleanest congruence coverage,
lowest reliance on q=3, and human-review priority. `(5,4,5)` stays capped at
`worth_human_modular_review`.

The cross-prime branch compatibility audit now checks the non-q=3 focused
primes q in `{13,17,41,61}` jointly. In the completed coefficient run, no
level-220 newform has a compatible unit/single-mask branch assignment across
all four non-q=3 primes, so the safe route label is
`cross_prime_elimination_candidate`. The q=3 exceptionality audit records that
q=3 is good relative to level 220, flags the q=3 reliance penalty, and classifies
q=3 as `q3_consistent_with_larger_primes` because the larger-prime cross-check
also closes the tracked assignments.

The quantifier-safety audit now checks the theorem-safe formulation of the
non-q=3 route. For each level-220 newform it asks whether there exists one
prime with complete same-prime branch coverage, instead of using a fixed branch
assignment across different primes. In the completed coefficient run, newform 0
has complete local branch coverage at q=17 and q=41, while newform 1 has
complete local branch coverage at q=13. The aggregate safe label is
`quantifier_safe_cross_prime_candidate`, still capped at
`worth_human_modular_review`.

The Frey-conductor proof audit now records the exact symbolic formulas for the
displayed Frey curve:
`c4 = 16*(A^10 + A^5*B^4 + B^8)`,
`c6 = 32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8)`,
`Delta = 16*A^10*B^8*C^10`, and
`j = 256*(A^10 + A^5*B^4 + B^8)^3/(A^10*B^8*C^10)`.
The conductor-support audit keeps level `220 = 2^2 * 5 * 11` as a candidate
level only: 2 and 5 need exact local conductor checks, 11 needs justification
because it is not forced by the displayed discriminant unless it divides ABC,
and primes dividing A, B, or C must be removed by level lowering. The bad-prime
Tate checklist and level-lowering obligation list keep the route validity score
at `conductor_gap_blocks_upgrade`.

The conductor-exponent and level-220 provenance audit makes that blocker more
explicit. Generic odd primes dividing A, B, or C away from 2, 5, and 11 are
modeled as multiplicative in the displayed template when `v_ell(c4)=0`, but
bad-prime exponents at 2, 5, and 11 still require human Tate analysis. The
aggregate level remains `level_220_heuristic_target`, the factor 11 is flagged
as `level_11_factor_unjustified`, and the A/B/C prime cases are flagged with
`abc_prime_removal_gap` until a level-lowering theorem removes them from the
comparison level. The optional Sage conductor sanity script is for formula and
synthetic-sample checks only.

The candidate-level discovery layer now stops assuming level 220. It generates
levels `2^a * 5^b * 11^c` for `a in {0,1,2,3}`, `b in {0,1,2}`, and
`c in {0,1}`, including variants without factor 11 and the current baseline
220. It writes `sage_candidate_level_expander_545.sage`, imports
`candidate_level_newforms_545.json` when available, applies unit and
single-mask trace filters across levels, and ranks candidate levels. Without
Sage data the aggregate label stays `level_data_insufficient`; if multiple
plausible levels show trace pressure the label becomes
`multi_level_trace_pressure_candidate`; if plausible levels have surviving
newforms the route is `level_sensitive_route`.

The Sage follow-up workflow now runs `sage_candidate_level_expander_545.sage`
after the level-220 coefficient expander and includes
`candidate_level_newforms_545.json`, the candidate-level import CSVs,
`trace_filter_across_levels_545.csv`, and `LEVEL_ROUTE_RANKING_545.md` in the
CI artifacts.

Missing invariant formulas downgrade to `needs_human_tate_algorithm`, missing
coefficients become `coefficient_missing`, and unapplied congruence assumptions
become `level_lowering_assumption_required`.

New proof obligation: Run the Tate algorithm / reduction analysis for the Frey
curve at q in `{3,13,17,41,61}` under A_only, B_only, and C_only.

Additional proof obligation: Justify that the multiplicative-reduction
branches satisfy the level-lowering congruence
`a_q(f) == +/-(q+1) mod 5` at q in `{3,13,17,41,61}`.

Additional review obligation: Justify the non-q=3 cross-prime branch
compatibility audit and review q=3 exceptionality.

Additional review obligation: Verify the quantifier-safe cross-prime route and
conditional theorem packet, including the assumption dependency graph and
adversarial review checklist.

Additional review obligation: Prove the Frey-conductor and level-lowering
package needed for the quantifier-safe trace elimination: Frey attachment,
minimal conductor at 2, 5, 11 and primes dividing ABC, residual mod-5
irreducibility, exact lowering to level 220, level-220 newform exhaustion, and
good-prime trace comparison validity.

Additional review obligation: Justify the provenance of `220 = 2^2 * 5 * 11`,
resolve `level_11_factor_unjustified`, and close `abc_prime_removal_gap` for
all primes dividing A, B, or C.

Additional review obligation: Run candidate-level target discovery before
treating 220 as the comparison level; import newform coefficients for generated
levels and decide whether the route is level-sensitive.

## Reproducibility Note

Generated `runs/` artifacts are intentionally ignored by Git to avoid turning
the repository into a data dump. Promote a run into documentation only after a
human or agent has interpreted the candidate clusters.
