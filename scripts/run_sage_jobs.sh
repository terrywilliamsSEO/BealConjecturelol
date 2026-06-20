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

JOB_DIR="$RUN_DIR/sage_jobs"
if [[ ! -d "$JOB_DIR" ]]; then
  echo "No sage_jobs directory found at: $JOB_DIR"
  exit 2
fi

for job in "$JOB_DIR"/sage_*.sage; do
  [[ -e "$job" ]] || continue
  echo "Running $job"
  sage "$job"
done

echo "Sage jobs finished. JSON outputs should be in $RUN_DIR/sage_results."
