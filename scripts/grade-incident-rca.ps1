<#
Deterministic grader for lightweight-incident-rca notes.
Usage: ./scripts/grade-incident-rca.ps1 -Path <candidate.md>
Emits JSON to stdout; exit 0 = pass, 1 = fail. No LLM, no network.
Checks mirror SKILL.md: 7 headings, timestamps, detection gap separate,
owned actions, blameless, concise, no secrets/log-dumps.
#>
param([Parameter(Mandatory=$true)][string]$Path)
$text = Get-Content -Path $Path -Raw
$lines = (Get-Content -Path $Path).Count
$fails = @()
function Has([string]$re) { return ($text -match "(?im)^\s*(#{1,4}\s*)?.*\b$re\b.*$") }
foreach ($h in @("Summary","Impact","Timeline","Root Cause","Detection Gap","Corrective Actions","Lessons")) {
  if (-not (Has $h)) { $fails += "missing-heading:$h" }
}
if ($text -notmatch "\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}\s*(EDT|EST|UTC)|2026-") { $fails += "missing-timestamp" }
if ($text -notmatch "(?i)completed|pending|deferred") { $fails += "actions-not-split" }
if ($text -notmatch "(?i)(PR\s*#\d+|OPS-\d+|runbook|docs/|alert|monitor|DLQ|gate|PR #)") { $fails += "actions-not-owned" }
$blame = @("blame","stupid","careless","lazy","incompetent","\bfault of\b")
foreach ($b in $blame) { if ($text -match "(?i)$b") { $fails += "blame-language:$b"; break } }
if ($text -match "(?i)ghp_[A-Za-z0-9]+|sk-(live|test)-|xox[bap]-|-----BEGIN .*PRIVATE KEY") { $fails += "possible-secret" }
if ($lines -gt 60) { $fails += "too-long:$lines-lines" }
$fenceBlocks = ([regex]::Matches($text, '```[\s\S]*?```'))
foreach ($m in $fenceBlocks) { if (($m.Value -split "`n").Count -gt 15) { $fails += "log-dump"; break } }
$pass = ($fails.Count -eq 0)
$result = [ordered]@{ file=$Path; lines=$lines; pass=$pass; fails=$fails }
$result | ConvertTo-Json -Compress
if ($pass) { exit 0 } else { exit 1 }
