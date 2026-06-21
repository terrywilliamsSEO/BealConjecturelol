# Sage/Newform Follow-Up Report

Output directory: `runs/sage_followup_ci`

## Guardrail

This pipeline exports Sage jobs, imports machine-readable Sage JSON, and updates route confidence. It does not certify theorem claims for Beal or any generalized Fermat case.

Every imported row sets `contradiction_claim_allowed` to `False`. The strongest review label is `worth_human_modular_review`, derived only from conservative `modular_followup_candidate` evidence.

## Counts

- Sage jobs generated: `13`.
- Sage import rows: `13`.
- Known-case Sage calibration rows: `19`.
- Known-case overpromotion rows: `0`.
- Sage status `completed`: `10`.
- Sage status `timeout`: `3`.
- Updated label `modular_followup_candidate`: `3`.
- Updated label `needs_external_sage_check`: `3`.
- Updated label `sage_checked_inconclusive`: `7`.

## Human Review Queue

| rank | signature | previous label | Sage status | trace status | updated label | priority |
| ---: | --- | --- | --- | --- | --- | ---: |
| 1 | `5-4-5` | `mixed_needs_external_check` | `completed` | `narrow` | `modular_followup_candidate` | 7.25 |
| 2 | `7-4-7` | `needs_external_sage_check` | `completed` | `narrow` | `modular_followup_candidate` | 7.0 |
| 3 | `4-7-7` | `needs_external_sage_check` | `completed` | `narrow` | `modular_followup_candidate` | 7.0 |
| 4 | `4-3-3` | `newform_check_candidate` | `completed` | `inconclusive` | `sage_checked_inconclusive` | 4.25 |
| 5 | `3-4-3` | `newform_check_candidate` | `completed` | `inconclusive` | `sage_checked_inconclusive` | 4.25 |
| 6 | `5-5-4` | `mixed_needs_external_check` | `completed` | `inconclusive` | `sage_checked_inconclusive` | 3.5 |
| 7 | `5-3-5` | `mixed_needs_external_check` | `completed` | `inconclusive` | `sage_checked_inconclusive` | 3.5 |
| 8 | `4-5-5` | `mixed_needs_external_check` | `completed` | `inconclusive` | `sage_checked_inconclusive` | 3.5 |
| 9 | `3-3-5` | `needs_external_sage_check` | `completed` | `inconclusive` | `sage_checked_inconclusive` | 3.5 |
| 10 | `3-3-4` | `needs_external_sage_check` | `completed` | `inconclusive` | `sage_checked_inconclusive` | 3.5 |
| 11 | `7-7-4` | `needs_external_sage_check` | `timeout` | `not_checked` | `needs_external_sage_check` | 1.5 |
| 12 | `5-5-7` | `mixed_needs_external_check` | `timeout` | `not_checked` | `needs_external_sage_check` | 1.5 |
| 13 | `3-5-5` | `needs_external_sage_check` | `timeout` | `not_checked` | `needs_external_sage_check` | 1.5 |

## Files

- `sage_job_manifest.csv`: generated Sage jobs and metadata.
- `sage_environment.json`: detected native, WSL, Docker, or CI execution mode.
- `sage_environment_report.md`: human-readable execution-mode report.
- `sage_execution_manifest.csv`: command hints for running each Sage job.
- `sage_import_results.csv`: validated Sage JSON imports or skip rows.
- `sage_known_case_calibration.csv`: known-case safety check after Sage import.
- `modular_confidence_summary.csv`: conservative confidence updates.
- `sage_roundtrip_summary.csv`: one-row-per-job import and review summary.
- `candidate_dossier_index.md`: dossier links for queued signatures.
- `sage_jobs/`: per-signature `.sage` jobs and batch runner.
- `sage_results/`: expected JSON output directory.

## Next Work

Run the generated Sage jobs with native Sage, WSL, Docker, or GitHub Actions, then run `python -m beal_rsg_lab.sage_followup_cli import` and `python -m beal_rsg_lab.sage_followup_cli summarize`.
