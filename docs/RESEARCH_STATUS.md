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
missing, WSL Sage timed out, and Docker was not found on PATH. Every job was
written and every import row was marked `unavailable`. This preserves the
conservative route label `needs_external_sage_check` and prevents missing
external data from becoming route confidence.

The generated queue contains 13 signatures, including the route-collision
signatures `(5,5,7)`, `(5,3,5)`, and `(5,4,5)`, plus the repeated
newform-check candidates `(3,4,3)` and `(4,3,3)`. Known artifacts remain
demoted and no known case is overpromoted after Sage import.

The committed dossier index is
[dossiers/candidate_dossier_index.md](dossiers/candidate_dossier_index.md).
The Docker runners and GitHub Actions workflow are now the preferred execution
paths when local Sage is absent.

## Reproducibility Note

Generated `runs/` artifacts are intentionally ignored by Git to avoid turning
the repository into a data dump. Promote a run into documentation only after a
human or agent has interpreted the candidate clusters.
