#!/usr/bin/env bash
set -euo pipefail

RUN_DIR="${1:-}"
IMAGE="${SAGE_DOCKER_IMAGE:-sagemath/sagemath:latest}"

if [[ -z "$RUN_DIR" ]]; then
  echo "Usage: scripts/run_sage_jobs_docker.sh <run-directory>"
  echo "Example: SAGE_DOCKER_IMAGE=sagemath/sagemath:latest scripts/run_sage_jobs_docker.sh runs/sage_followup_20260620_183000"
  exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker was not found on PATH."
  echo "Install Docker Desktop, start the Docker service, or use native/WSL Sage instead."
  exit 0
fi

if [[ ! -f "$RUN_DIR/sage_job_manifest.csv" ]]; then
  echo "No Sage job manifest found at $RUN_DIR/sage_job_manifest.csv"
  exit 2
fi

SAGE_DOCKER_IMAGE="$IMAGE" python -m beal_rsg_lab.sage_followup_cli roundtrip \
  --run-dir "$RUN_DIR" \
  --skip-generate \
  --backend docker \
  --timeout-seconds "${SAGE_JOB_TIMEOUT_SECONDS:-600}" \
  --dossier-dir "$RUN_DIR/dossiers"

echo "Docker Sage jobs finished. JSON outputs should be in $RUN_DIR/sage_results."
