#!/usr/bin/env bash
set -euo pipefail

RUN_DIR="${1:-}"
if [[ -z "$RUN_DIR" ]]; then
  echo "Usage: scripts/run_sage_jobs.sh <run-directory>"
  echo "Example: scripts/run_sage_jobs.sh runs/sage_followup_20260620_183000"
  exit 2
fi

if ! command -v sage >/dev/null 2>&1; then
  echo "SageMath executable was not found on PATH. Install SageMath or run via Docker, then retry."
  exit 0
fi

if [[ ! -f "$RUN_DIR/sage_job_manifest.csv" ]]; then
  echo "No Sage job manifest found at: $RUN_DIR/sage_job_manifest.csv"
  exit 2
fi

python -m beal_rsg_lab.sage_followup_cli roundtrip \
  --run-dir "$RUN_DIR" \
  --skip-generate \
  --backend native_sage \
  --timeout-seconds "${SAGE_JOB_TIMEOUT_SECONDS:-600}" \
  --dossier-dir "$RUN_DIR/dossiers"

echo "Sage jobs finished. JSON outputs should be in $RUN_DIR/sage_results."
