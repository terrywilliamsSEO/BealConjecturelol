# Known-Case Calibration Report

Note: this report records the pre-theorem-terrain calibration pass. The FLT
diagonal mismatch described here is superseded by
[theorem_terrain_20260620_174500.md](theorem_terrain_20260620_174500.md), where
diagonal FLT-style signatures route correctly to theorem terrain.

Run folder:

```text
runs/known_case_calibration_20260620_163000
```

Command:

```powershell
python run_experiment.py --prime-limit 31 --control-samples 16 --timestamp known_case_calibration_20260620_163000
```

## Guardrail

This is a calibration report, not a theorem database. The known-case library is
deliberately modest and contains citation placeholders for later replacement.
The point of this phase is to test whether RSG recognizes route shapes and
avoids false breakthroughs before returning to Beal discovery mode.

## Counts

- Sweep rows: `2160`.
- Known/calibration cases: `19`.
- `known_case_mismatch`: `6`.
- `artifact_like`: `2`.
- `needs_external_sage_check`: `10`.
- `not_promising_yet`: `1`.
- `calibrated_route_candidate`: `0`.
- Sage available: `False`.
- Sage scripts exported: `11`.

## Route Confusion Matrix

| bucket | cases | interpretation |
| --- | ---: | --- |
| `known_impossible_system_weak` | 4 | Diagonal FLT-style cases were not recognized by current RSG signals. |
| `false_negative` | 2 | Expected descent/modular bridge cases stayed weak. |
| `modular_method_correctly_routed` | 10 | Modular-method calibration cases were routed to external Sage follow-up. |
| `artifact_correctly_demoted` | 2 | Order-two subgroup artifact calibrators were demoted. |
| `uncertain_case` | 1 | The imprimitive `(3,3,4)` calibration case stayed non-promoted. |

## Main Findings

The useful positive result is artifact discipline. The two artifact calibrators
`(11,11,13)` and `(11,11,5)` are labeled `artifact_like`, matching the previous
order-two subgroup explanation.

The useful negative result is that the engine still does not know FLT terrain.
The diagonal cases `(3,3,3)`, `(4,4,4)`, `(5,5,5)`, and `(7,7,7)` are marked
`known_case_mismatch` because the current RSG layers see them as locally weak or
control-like rather than recognizing the separate FLT proof shape.

Ten modular-method-style cases are routed to `needs_external_sage_check`, not
to proof claims. The highest route-prior sketches are:

| rank | signature | label | readiness | artifact likelihood |
| ---: | --- | --- | ---: | ---: |
| 1 | `(3,3,5)` | `needs_external_sage_check` | 3.36 | 0.0 |
| 2 | `(3,4,3)` | `needs_external_sage_check` | 3.22 | 0.0 |
| 3 | `(3,5,5)` | `needs_external_sage_check` | 3.1433333333 | 0.0 |
| 4 | `(7,7,4)` | `needs_external_sage_check` | 2.9109090909 | 0.0 |
| 5 | `(4,7,7)` | `needs_external_sage_check` | 2.8654545455 | 0.0 |

## Sage Exports

Sage is not available locally, so the harness wrote optional `.sage` scripts
instead of running newform checks. The manifest records
`script_written_sage_unavailable` for each export. These scripts compute
finite-field point counts and traces for candidate Frey-style curves and
include placeholders for later conductor/newform work.

## Interpretation

The engine is now a better research instrument than before, but it is not ready
to promote Beal discoveries. The next calibration improvement should add a
known-proof recognizer for diagonal FLT/descent terrain, or at least a route
label that explicitly hands diagonal cases to the FLT-style proof family rather
than treating them as weak local data.

Until that calibration debt is paid, new Beal candidates should remain gated
behind `needs_external_sage_check` or `not_promising_yet`, not promoted as
`calibrated_route_candidate`.
