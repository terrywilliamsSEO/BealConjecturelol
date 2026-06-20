# Sage/Newform Follow-Up

The Sage follow-up loop turns `needs_external_sage_check` and related route
labels into executable Sage jobs and machine-readable JSON imports. It is a
calibration and triage tool only. It does not certify theorem claims for Beal.

## Default Behavior

`run_experiment.py` always writes:

- `sage_environment.json`
- `sage_environment_report.md`
- `sage_job_manifest.csv`
- `sage_execution_manifest.csv`
- `sage_import_results.csv`
- `sage_known_case_calibration.csv`
- `modular_confidence_summary.csv`
- `sage_roundtrip_summary.csv`
- `candidate_dossier_index.md`
- `README_SAGE_FOLLOWUP_REPORT.md`
- `sage_jobs/`
- `sage_results/`

If SageMath is not installed, the run still passes. Jobs are written and import
rows are marked `unavailable`.

## CLI Roundtrip

Use the module CLI for repeatable operations:

```powershell
python -m beal_rsg_lab.sage_followup_cli detect --run-dir runs\<run-id>
python -m beal_rsg_lab.sage_followup_cli generate --timestamp sage_followup_local
python -m beal_rsg_lab.sage_followup_cli run --run-dir runs\<run-id> --backend native_sage
python -m beal_rsg_lab.sage_followup_cli import --run-dir runs\<run-id>
python -m beal_rsg_lab.sage_followup_cli summarize --run-dir runs\<run-id>
python -m beal_rsg_lab.sage_followup_cli roundtrip --run-dir runs\<run-id> --skip-generate --backend docker
```

`detect` writes `sage_environment.json` and `sage_environment_report.md`.
`run` executes the smoke job and generated jobs with per-job timeout JSON.
`import` refreshes Sage JSON imports, modular confidence, known-case safety, and
roundtrip summaries. `summarize` writes dossiers under `docs/dossiers/` by
default. `roundtrip` chains detection, optional generation, execution, import,
and dossier generation.

## Running Sage Jobs

After an experiment creates a run directory, run one of:

```bash
scripts/run_sage_jobs.sh runs/<run-id>
```

```powershell
.\scripts\run_sage_jobs.ps1 -RunDir runs\<run-id>
```

If Sage is installed in WSL, run the batch file directly from a WSL shell:

```bash
sage runs/<run-id>/sage_jobs/run_all_sage_jobs.sage
```

The scripts execute each `sage_jobs/sage_*.sage` file and write JSON to
`sage_results/`. Rerun the experiment or importer after the JSON files exist to
refresh the confidence tables.

## Docker Option

If a local Sage install is inconvenient, run the jobs in a SageMath container and
mount the repository directory. The exact image name can vary by platform, but
the workflow is:

```bash
SAGE_DOCKER_IMAGE=sagemath/sagemath:latest bash scripts/run_sage_jobs_docker.sh runs/<run-id>
```

```powershell
$env:SAGE_DOCKER_IMAGE = "sagemath/sagemath:latest"
.\scripts\run_sage_jobs_docker.ps1 -RunDir runs\<run-id>
```

The Docker image can be changed with `SAGE_DOCKER_IMAGE`. The scripts fail
gracefully if Docker is unavailable.

## GitHub Actions

`.github/workflows/sage-followup.yml` can generate jobs, run them through Docker,
import JSON results, verify conservative labels, and upload `sage_results/` as
an artifact. The workflow is also manually dispatchable with a custom run ID.

## JSON Contract

Each Sage result should include:

- `job_id`
- `signature`
- `sage_status`: `completed`, `partial`, `failed`, `timeout`, or `unavailable`
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

In roundtrip summaries, `modular_followup_candidate` is surfaced as the review
label `worth_human_modular_review`.

## Smoke And Timeout Behavior

Every execution backend runs `sage_smoke.sage` before the real queue. The smoke
job checks that Sage starts, finite-field elliptic curve point counts work, and
JSON can be written. If the smoke job fails, times out, or is unavailable, the
real queue is not executed.

If a real job times out, the Python runner writes importer-compatible JSON with
`sage_status = "timeout"` and `contradiction_claim_allowed = false`. This keeps
the roundtrip auditable even when a backend is too slow.

## Dossiers

Candidate dossiers live under [dossiers/](dossiers/). Each dossier records the
signature, normalized form, known-case terrain, artifact risk, p-adic status,
Frey-template confidence, Sage job/result status, the reason no theorem claim is
available, and the recommended next mathematical check.
