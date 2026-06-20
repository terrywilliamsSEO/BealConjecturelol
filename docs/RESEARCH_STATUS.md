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

## Reproducibility Note

Generated `runs/` artifacts are intentionally ignored by Git to avoid turning
the repository into a data dump. Promote a run into documentation only after a
human or agent has interpreted the candidate clusters.
