param(
  [string]$Repo,
  [string]$Branch = "main",
  [string]$SkillsRoot = "C:\Users\86180\.codex\skills"
)

$ErrorActionPreference = "Stop"

function Find-Exe {
  param(
    [string]$Name,
    [string[]]$Candidates
  )

  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) {
    return $cmd.Source
  }

  foreach ($candidate in $Candidates) {
    if (Test-Path -LiteralPath $candidate) {
      return $candidate
    }
  }

  throw "Cannot find $Name."
}

function Write-JsonFile {
  param(
    [object]$Value,
    [string]$Path,
    [int]$Depth = 10
  )

  $json = $Value | ConvertTo-Json -Depth $Depth
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $json, $utf8NoBom)
}

$Gh = Find-Exe "gh.exe" @("C:\Program Files\GitHub CLI\gh.exe")
$Git = Find-Exe "git.exe" @(
  "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe",
  "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\mingw64\bin\git.exe",
  "C:\Program Files\Git\cmd\git.exe"
)
$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) "codex-skills-gh-api"

function Read-GitBlobBytes {
  param([string]$BlobSha)

  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $Git
  $psi.Arguments = "cat-file blob $BlobSha"
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true

  $process = [System.Diagnostics.Process]::Start($psi)
  $memory = New-Object System.IO.MemoryStream
  $process.StandardOutput.BaseStream.CopyTo($memory)
  $stderr = $process.StandardError.ReadToEnd()
  $process.WaitForExit()

  if ($process.ExitCode -ne 0) {
    throw "Cannot read Git blob $BlobSha. $stderr"
  }

  return $memory.ToArray()
}

if (-not $Repo) {
  throw "Repo is required, for example sannnnway-prog/seo-page-factory."
}

if (-not (Test-Path -LiteralPath $TempDir)) {
  New-Item -ItemType Directory -Path $TempDir | Out-Null
}

Set-Location -LiteralPath $SkillsRoot

$ref = & $Gh api "repos/$Repo/git/ref/heads/$Branch" | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or -not $ref.object.sha) {
  throw "Cannot read remote ref heads/$Branch for $Repo."
}
$baseCommit = $ref.object.sha

$commit = & $Gh api "repos/$Repo/git/commits/$baseCommit" | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or -not $commit.tree.sha) {
  throw "Cannot read base commit $baseCommit."
}
$baseTree = $commit.tree.sha

$remoteTree = & $Gh api "repos/$Repo/git/trees/$baseTree`?recursive=1" | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) {
  throw "Cannot read base tree $baseTree."
}

$localEntriesRaw = & $Git ls-files -s
if ($LASTEXITCODE -ne 0) {
  throw "Cannot list local tracked skill files."
}

$localEntries = New-Object System.Collections.Generic.List[object]
foreach ($line in $localEntriesRaw) {
  if ($line -match "^(\d+)\s+([0-9a-f]{40})\s+\d+\t(.+)$") {
    $localEntries.Add([pscustomobject]@{
      mode = $Matches[1]
      sha = $Matches[2]
      path = $Matches[3]
    }) | Out-Null
  }
}

$localPathSet = @{}
foreach ($entry in $localEntries) {
  if ($entry.path) {
    $localPathSet[$entry.path] = $true
  }
}

$tree = New-Object System.Collections.Generic.List[object]
$index = 0
foreach ($entry in $localEntries) {
  if (-not $entry.path) {
    continue
  }

  $index += 1
  $path = $entry.path
  Write-Host "Uploading blob $index/$($localEntries.Count): $path"

  $bytes = Read-GitBlobBytes $entry.sha
  $blobBody = @{
    content = [Convert]::ToBase64String($bytes)
    encoding = "base64"
  }
  $blobJson = Join-Path $TempDir "blob.json"
  Write-JsonFile $blobBody $blobJson 5
  $blob = & $Gh api "repos/$Repo/git/blobs" --method POST --input $blobJson | ConvertFrom-Json
  if ($LASTEXITCODE -ne 0 -or -not $blob.sha) {
    throw "Cannot upload blob for $path."
  }

  $tree.Add([pscustomobject]@{
    path = $path
    mode = "100644"
    type = "blob"
    sha = $blob.sha
  }) | Out-Null
}

foreach ($entry in $remoteTree.tree) {
  if ($entry.type -eq "blob" -and -not $localPathSet.ContainsKey($entry.path)) {
    $tree.Add([pscustomobject]@{
      path = $entry.path
      mode = "100644"
      type = "blob"
      sha = $null
    }) | Out-Null
  }
}

$treeBody = @{
  base_tree = $baseTree
  tree = $tree
}
$treeJson = Join-Path $TempDir "tree.json"
Write-JsonFile $treeBody $treeJson 20
$newTree = & $Gh api "repos/$Repo/git/trees" --method POST --input $treeJson | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or -not $newTree.sha) {
  throw "Cannot create Git tree."
}

$messageStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss K"
$commitBody = @{
  message = "Sync all Codex skills $messageStamp"
  tree = $newTree.sha
  parents = @($baseCommit)
}
$commitJson = Join-Path $TempDir "commit.json"
Write-JsonFile $commitBody $commitJson 10
$newCommit = & $Gh api "repos/$Repo/git/commits" --method POST --input $commitJson | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or -not $newCommit.sha) {
  throw "Cannot create Git commit."
}

$refBody = @{
  sha = $newCommit.sha
  force = $false
}
$refJson = Join-Path $TempDir "ref.json"
Write-JsonFile $refBody $refJson 5
& $Gh api "repos/$Repo/git/refs/heads/$Branch" --method PATCH --input $refJson | Out-Null
if ($LASTEXITCODE -ne 0) {
  throw "Cannot update remote branch. It may have changed; rerun sync-skills.ps1 to use the new base."
}

Write-Host "Updated https://github.com/$Repo/commit/$($newCommit.sha)"
