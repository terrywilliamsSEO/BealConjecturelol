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

## Reproducibility Note

Generated `runs/` artifacts are intentionally ignored by Git to avoid turning
the repository into a data dump. Promote a run into documentation only after a
human or agent has interpreted the candidate clusters.
