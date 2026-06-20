# Agent Guide

This repository should stay useful to future agents. Keep claims modest, keep
outputs structured, and make each experiment reproducible.

## Important Commands

```powershell
python -m unittest discover
python run_experiment.py --prime-limit 31 --control-samples 16
python run_experiment.py --primes 5,7,11 --control-samples 6 --no-lift
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
- `beal_rsg_lab/rsg_modular_shadow.py`: symbolic obstruction and clustering.
- `beal_rsg_lab/run_experiment.py`: orchestration and file outputs.
- `tests/`: deterministic unit and smoke tests.

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
