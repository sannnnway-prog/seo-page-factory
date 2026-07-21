param(
  [string]$Repo = $env:CODEX_SKILLS_REPO,
  [string]$RepoName = "codex-skills",
  [switch]$Public
)

$ErrorActionPreference = "Stop"

function Invoke-Checked {
  param(
    [string]$FilePath,
    [string[]]$Arguments,
    [string]$FailureMessage
  )

  & $FilePath @Arguments
  if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine($FailureMessage)
    exit 1
  }
}

function Test-GitHubRepo {
  param([string]$NameWithOwner)

  $previousPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  & $Gh repo view $NameWithOwner *> $null
  $exitCode = $LASTEXITCODE
  $ErrorActionPreference = $previousPreference
  return ($exitCode -eq 0)
}

function Test-GitHubPath {
  param(
    [string]$NameWithOwner,
    [string]$Path
  )

  $previousPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  & $Gh api "repos/$NameWithOwner/contents/$Path" --silent *> $null
  $exitCode = $LASTEXITCODE
  $ErrorActionPreference = $previousPreference
  return ($exitCode -eq 0)
}

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

  throw "Cannot find $Name. Add it to PATH or update sync-skills.ps1."
}

$Gh = Find-Exe "gh.exe" @(
  "C:\Program Files\GitHub CLI\gh.exe"
)

$Git = Find-Exe "git.exe" @(
  "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe",
  "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\mingw64\bin\git.exe",
  "C:\Program Files\Git\cmd\git.exe"
)
$GitDir = Split-Path -Parent $Git
if (($env:PATH -split ";") -notcontains $GitDir) {
  $env:PATH = "$GitDir;$env:PATH"
}

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $Root

Invoke-Checked $Gh @("auth", "status") "GitHub CLI is not authenticated. Run: gh auth login"

$Owner = (& $Gh api user --jq ".login")
if ($LASTEXITCODE -ne 0 -or -not $Owner) {
  throw "Cannot read the authenticated GitHub user. Check GitHub CLI auth and network access."
}
$Owner = $Owner.Trim()
if (-not $Repo) {
  $preferredRepo = "$Owner/$RepoName"
  if (Test-GitHubRepo $preferredRepo) {
    $Repo = $preferredRepo
  } else {
    $repoList = & $Gh repo list $Owner --limit 100 --json nameWithOwner --jq ".[].nameWithOwner"
    if ($LASTEXITCODE -ne 0) {
      [Console]::Error.WriteLine("Cannot list GitHub repositories for $Owner.")
      exit 1
    }

    foreach ($candidate in $repoList) {
      if (Test-GitHubPath $candidate "feature-page-factory/SKILL.md") {
        $Repo = $candidate
        Write-Host "Detected existing skill repository: $Repo"
        break
      }
    }

    if (-not $Repo) {
      $Repo = $preferredRepo
    }
  }
}

if (-not (Test-Path -LiteralPath ".git")) {
  Invoke-Checked $Git @("init") "Cannot initialize local skills Git repository."
  Invoke-Checked $Git @("checkout", "-B", "main") "Cannot create local main branch."
}

Invoke-Checked $Git @("config", "user.name", "Codex Skill Sync") "Cannot configure local Git user.name."
Invoke-Checked $Git @("config", "user.email", "codex-skill-sync@users.noreply.github.com") "Cannot configure local Git user.email."

$repoExists = $true
try {
  & $Gh repo view $Repo 1>$null
} catch {
  $repoExists = $false
}

if (-not $repoExists) {
  $visibility = if ($Public) { "--public" } else { "--private" }
  & $Gh repo create $Repo $visibility
  if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine("Cannot create GitHub repository $Repo.")
    exit 1
  }
  $remoteUrl = "https://github.com/$Repo.git"
  $remotes = (& $Git remote)
  if ($remotes -contains "origin") {
    Invoke-Checked $Git @("remote", "set-url", "origin", $remoteUrl) "Cannot update origin remote."
  } else {
    Invoke-Checked $Git @("remote", "add", "origin", $remoteUrl) "Cannot add origin remote."
  }
} else {
  $remoteUrl = "https://github.com/$Repo.git"
  $remotes = (& $Git remote)
  if ($remotes -contains "origin") {
    Invoke-Checked $Git @("remote", "set-url", "origin", $remoteUrl) "Cannot update origin remote."
  } else {
    Invoke-Checked $Git @("remote", "add", "origin", $remoteUrl) "Cannot add origin remote."
  }
}

$defaultBranch = "main"
try {
  $viewBranch = (& $Gh repo view $Repo --json defaultBranchRef --jq ".defaultBranchRef.name").Trim()
  if ($viewBranch) {
    $defaultBranch = $viewBranch
  }
} catch {
  $defaultBranch = "main"
}

Invoke-Checked $Git @("checkout", "-B", $defaultBranch) "Cannot switch to $defaultBranch."

$hasRemoteBranch = $false
$fetchOutput = & $Git fetch origin $defaultBranch 2>&1
$fetchExitCode = $LASTEXITCODE
if ($fetchExitCode -eq 0) {
  $hasRemoteBranch = $true
} elseif (($fetchOutput -join "`n") -match "couldn't find remote ref|could not find remote ref|fatal: couldn't find remote ref") {
  $hasRemoteBranch = $false
} else {
  [Console]::Error.WriteLine("Cannot fetch remote branch $defaultBranch from $Repo.")
  [Console]::Error.WriteLine(($fetchOutput -join [Environment]::NewLine))
  exit 1
}

if ($hasRemoteBranch) {
  & $Git diff --quiet HEAD "origin/$defaultBranch"
  $treeDiffExitCode = $LASTEXITCODE

  if ($treeDiffExitCode -eq 0) {
    $divergence = (& $Git rev-list --left-right --count "HEAD...origin/$defaultBranch").Trim()
    if ($divergence -and $divergence -ne "0`t0" -and $divergence -ne "0 0") {
      Write-Host "Local and remote trees match; aligning local branch pointer to origin/$defaultBranch."
      Invoke-Checked $Git @("reset", "--soft", "origin/$defaultBranch") "Cannot align local branch pointer to origin/$defaultBranch."
    }
  } else {
  $mergeBase = ""
  try {
    $mergeBase = (& $Git merge-base HEAD "origin/$defaultBranch").Trim()
  } catch {
    $mergeBase = ""
  }

  if ($mergeBase) {
    Invoke-Checked $Git @("pull", "--rebase", "--autostash", "origin", $defaultBranch) "Remote changes conflict with local skills. Resolve the conflict, then rerun sync-skills.ps1."
  } else {
    Invoke-Checked $Git @("merge", "--allow-unrelated-histories", "--no-edit", "origin/$defaultBranch") "Remote changes conflict with local skills. Resolve the conflict, then rerun sync-skills.ps1."
  }
  }
}

$conflicts = & $Git grep -n -E "^(<<<<<<<|=======|>>>>>>>)"
if ($LASTEXITCODE -eq 0 -and $conflicts) {
  [Console]::Error.WriteLine("Conflict markers found. Resolve these files before syncing:")
  [Console]::Error.WriteLine(($conflicts -join [Environment]::NewLine))
  exit 1
}

Invoke-Checked $Git @("add", "-A") "Cannot stage local skill changes."
$pending = (& $Git status --porcelain)
if ($pending) {
  $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss K"
  Invoke-Checked $Git @("commit", "-m", "Sync Codex skills $stamp") "Cannot commit local skill changes."
} else {
  Write-Host "No local skill changes to commit."
}

$pushOutput = & $Git push -u origin $defaultBranch 2>&1
if ($LASTEXITCODE -ne 0) {
  [Console]::Error.WriteLine("Git push failed; trying GitHub API fallback.")
  [Console]::Error.WriteLine(($pushOutput -join [Environment]::NewLine))

  $apiFallback = Join-Path $Root "push-skills-via-gh-api.ps1"
  if (-not (Test-Path -LiteralPath $apiFallback)) {
    [Console]::Error.WriteLine("Cannot find API fallback script: $apiFallback")
    exit 1
  }

  & powershell -ExecutionPolicy Bypass -File $apiFallback -Repo $Repo -Branch $defaultBranch -SkillsRoot $Root
  if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine("GitHub API fallback failed.")
    exit 1
  }
}
Write-Host "Synced skills to https://github.com/$Repo"
