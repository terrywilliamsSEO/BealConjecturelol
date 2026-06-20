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

## Reproducibility Note

Generated `runs/` artifacts are intentionally ignored by Git to avoid turning
the repository into a data dump. Promote a run into documentation only after a
human or agent has interpreted the candidate clusters.
