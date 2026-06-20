param(
    [Parameter(Mandatory = $true)]
    [string]$RunDir
)

$sage = Get-Command sage -ErrorAction SilentlyContinue
if (-not $sage) {
    Write-Host "SageMath executable was not found on PATH. Install SageMath or run via Docker, then retry."
    exit 0
}

$jobDir = Join-Path $RunDir "sage_jobs"
if (-not (Test-Path -LiteralPath $jobDir -PathType Container)) {
    Write-Error "No sage_jobs directory found at: $jobDir"
    exit 2
}

Get-ChildItem -LiteralPath $jobDir -Filter "sage_*.sage" | ForEach-Object {
    Write-Host "Running $($_.FullName)"
    & $sage.Source $_.FullName
}

Write-Host "Sage jobs finished. JSON outputs should be in $(Join-Path $RunDir 'sage_results')."
