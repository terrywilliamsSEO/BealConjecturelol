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

$batch = Join-Path $RunDir "sage_jobs\run_all_sage_jobs.sage"
if (-not (Test-Path -LiteralPath $batch -PathType Leaf)) {
    Write-Error "No Sage batch file found at $batch"
    exit 2
}

$repoRoot = (Get-Location).Path
& $docker.Source run --rm `
    -v "${repoRoot}:/work" `
    -w /work `
    $image `
    sage "$($RunDir -replace '\\','/')/sage_jobs/run_all_sage_jobs.sage"

Write-Host "Docker Sage jobs finished. JSON outputs should be in $(Join-Path $RunDir 'sage_results')."
