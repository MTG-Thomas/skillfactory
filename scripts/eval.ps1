#!/usr/bin/env pwsh
# Thin eval driver: baseline vs skill vs candidate. Preserves raw artifacts under runs/.
# Requires: jcode (first-class), codex/opencode optional for cross-harness.
param([string]$Skill = "lightweight-incident-rca", [int]$Trials = 3)
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$dir = "runs/$ts-$Skill"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
Write-Host "Run dir: $dir (skill=$Skill trials=$Trials)"
Write-Host "TODO: drive 'jcode run --json --ndjson --trace' per case x trial, then deterministic grade.sh"
