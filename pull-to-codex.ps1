$ErrorActionPreference = "Stop"
$CodexSkillsRoot = "C:\Users\86180\.codex\skills"
$Skills = @(
  "feature-page-factory",
  "agnes-video",
  "ark-seedream-image",
  "openai-next-image",
  "gpt-image",
  "globalgpt",
  "globalgpt-coding",
  "globalgpt-image",
  "globalgpt-video",
  "ai-product-workflow",
  "figma-create-design-system-rules",
  "awesome-design-md"
)

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $RepoRoot

git pull --rebase
foreach ($skill in $Skills) {
  $source = Join-Path $RepoRoot $skill
  $destination = Join-Path $CodexSkillsRoot $skill
  if (-not (Test-Path -LiteralPath $source)) {
    throw "Missing skill folder in repo: $skill"
  }
  if (Test-Path -LiteralPath $destination) {
    Remove-Item -LiteralPath $destination -Recurse -Force
  }
  Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
}
Write-Host "Pulled $($Skills.Count) skills into $CodexSkillsRoot"