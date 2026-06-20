# Sage/Newform Follow-Up

The Sage follow-up loop turns `needs_external_sage_check` and related route
labels into executable Sage jobs and machine-readable JSON imports. It is a
calibration and triage tool only. It does not certify theorem claims for Beal.

## Default Behavior

`run_experiment.py` always writes:

- `sage_job_manifest.csv`
- `sage_import_results.csv`
- `sage_known_case_calibration.csv`
- `modular_confidence_summary.csv`
- `README_SAGE_FOLLOWUP_REPORT.md`
- `sage_jobs/`
- `sage_results/`

If SageMath is not installed, the run still passes. Jobs are written and import
rows are marked `unavailable`.

## Running Sage Jobs

After an experiment creates a run directory, run one of:

```bash
scripts/run_sage_jobs.sh runs/<run-id>
```

```powershell
.\scripts\run_sage_jobs.ps1 -RunDir runs\<run-id>
```

The scripts execute each `sage_jobs/sage_*.sage` file and write JSON to
`sage_results/`. Rerun the experiment or importer after the JSON files exist to
refresh the confidence tables.

## Docker Option

If a local Sage install is inconvenient, run the jobs in a SageMath container and
mount the repository directory. The exact image name can vary by platform, but
the workflow is:

```bash
docker run --rm -it -v "$PWD:/work" -w /work sagemath/sagemath sage runs/<run-id>/sage_jobs/run_all_sage_jobs.sage
```

On Windows PowerShell, use `${PWD}` for the mounted path.

## JSON Contract

Each Sage result should include:

- `job_id`
- `signature`
- `sage_status`: `completed`, `partial`, `failed`, or `unavailable`
- `checked_levels`
- `newform_count`
- `trace_match_status`
- `contradiction_claim_allowed`

`contradiction_claim_allowed` must be `false`. The importer rejects rows that try
to set it to true.

## Conservative Labels

Sage import can move a row only to:

- `needs_external_sage_check`
- `sage_checked_inconclusive`
- `modular_followup_candidate`
- `artifact_like`
- `not_promising_yet`

The strongest label, `modular_followup_candidate`, means the signature is worth
human modular-method review. It is not a proof label.
