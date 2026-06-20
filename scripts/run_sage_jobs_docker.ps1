param(
    [Parameter(Mandatory = $true)]
    [string]$RunDir
)

$image = if ($env:SAGE_DOCKER_IMAGE) { $env:SAGE_DOCKER_IMAGE } else { "sagemath/sagemath:latest" }
$docker = Get-Command docker -ErrorAction SilentlyContinue
if (-not $docker) {
    Write-Host "Docker was not found on PATH."
    Write-Host "Install Docker Desktop, start the Docker service, or use native/WSL Sage instead."
    exit 0
}

$manifest = Join-Path $RunDir "sage_job_manifest.csv"
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) {
    Write-Error "No Sage job manifest found at $manifest"
    exit 2
}

$env:SAGE_DOCKER_IMAGE = $image
$timeout = if ($env:SAGE_JOB_TIMEOUT_SECONDS) { $env:SAGE_JOB_TIMEOUT_SECONDS } else { "600" }
python -m beal_rsg_lab.sage_followup_cli roundtrip `
    --run-dir $RunDir `
    --skip-generate `
    --backend docker `
    --timeout-seconds $timeout `
    --dossier-dir (Join-Path $RunDir "dossiers")

Write-Host "Docker Sage jobs finished. JSON outputs should be in $(Join-Path $RunDir 'sage_results')."
