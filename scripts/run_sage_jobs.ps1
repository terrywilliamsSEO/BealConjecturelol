param(
    [Parameter(Mandatory = $true)]
    [string]$RunDir
)

$sage = Get-Command sage -ErrorAction SilentlyContinue
if (-not $sage) {
    Write-Host "SageMath executable was not found on PATH. Install SageMath or run via Docker, then retry."
    exit 0
}

$manifest = Join-Path $RunDir "sage_job_manifest.csv"
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) {
    Write-Error "No Sage job manifest found at $manifest"
    exit 2
}

$timeout = if ($env:SAGE_JOB_TIMEOUT_SECONDS) { $env:SAGE_JOB_TIMEOUT_SECONDS } else { "600" }
python -m beal_rsg_lab.sage_followup_cli roundtrip `
    --run-dir $RunDir `
    --skip-generate `
    --backend native_sage `
    --timeout-seconds $timeout `
    --dossier-dir (Join-Path $RunDir "dossiers")

Write-Host "Sage jobs finished. JSON outputs should be in $(Join-Path $RunDir 'sage_results')."
