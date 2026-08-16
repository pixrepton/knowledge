$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$required = @(
  'INDEX.md',
  'CONTROL_PLANE.md',
  'memory/OPERATOR_DECISIONS.md',
  'memory/ACTIVE_WORKSPACE.md',
  'memory/BACKLOG.md',
  'docs/AI_OS_ROADMAP.md'
)
foreach ($r in $required) {
  if (-not (Test-Path $r)) {
    Write-Error "missing $r"
    exit 1
  }
}
$aw = Get-Content -Raw 'memory/ACTIVE_WORKSPACE.md'
if ($aw -notmatch 'STAGED_ACTIVATION_AUTHORIZED') {
  Write-Error 'ACTIVE missing STAGED_ACTIVATION_AUTHORIZED'
  exit 1
}
if ($aw -notmatch 'REJECTED_BY_OPERATOR') {
  Write-Error 'ACTIVE missing REJECTED_BY_OPERATOR'
  exit 1
}
if ($aw -notmatch 'FACT-SUPERSESSION-WRITE-01') {
  Write-Error 'ACTIVE missing FACT write residual'
  exit 1
}
$bl = Get-Content -Raw 'memory/BACKLOG.md'
if ($bl -match 'OPERATOR_DECISION_REQUIRED') {
  Write-Error 'BACKLOG still says OPERATOR_DECISION_REQUIRED'
  exit 1
}
Write-Host 'knowledge-docs-sync-A PASS'
exit 0
