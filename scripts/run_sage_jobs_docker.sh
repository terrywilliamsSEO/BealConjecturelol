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

if [[ ! -f "$RUN_DIR/sage_jobs/run_all_sage_jobs.sage" ]]; then
  echo "No Sage batch file found at $RUN_DIR/sage_jobs/run_all_sage_jobs.sage"
  exit 2
fi

docker run --rm \
  -v "$PWD:/work" \
  -w /work \
  "$IMAGE" \
  sage "$RUN_DIR/sage_jobs/run_all_sage_jobs.sage"

echo "Docker Sage jobs finished. JSON outputs should be in $RUN_DIR/sage_results."
