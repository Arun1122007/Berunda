# ============================================================
# clone_repositories.ps1 — Repository Acquisition (PowerShell)
# Project Berunda — Karnataka State Police Datathon 2026
#
# Shallow clones Git repos into repositories/<owner>__<repo>/
# with commit pinning, license detection, and secrets scanning.
# ============================================================

param(
    [switch]$DryRun = $true,
    [string]$ResourceId = "",
    [string]$Priority = "",
    [long]$MaxFileSize = 209715200,
    [long]$MaxTotalSize = 1073741824,
    [switch]$Resume,
    [switch]$Force,
    [string]$WorkspaceRoot = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

$ErrorActionPreference = "Continue"

$ReposDir = Join-Path $WorkspaceRoot "repositories"
$ManifestsDir = Join-Path $WorkspaceRoot "manifests"
$LogFile = Join-Path $WorkspaceRoot "logs" "acquisition.log"

# Git repos to clone
$GitResources = @{
    "R026" = @{ url = "https://github.com/alephdata/followthemoney"; name = "FollowTheMoney schema"; classification = "REFERENCE" }
    "R027" = @{ url = "https://github.com/keplergl/kepler.gl"; name = "Kepler.gl"; classification = "REFERENCE" }
    "R030" = @{ url = "https://github.com/maplibre/maplibre-gl-js"; name = "MapLibre GL JS"; classification = "REFERENCE" }
}

# Secrets patterns (regex)
$SecretPatterns = @(
    '(?i)(api[_-]?key|apikey)\s*[:=]\s*[''"][a-zA-Z0-9]{16,}',
    '(?i)(secret|password|passwd|pwd)\s*[:=]\s*[''"][^\s''"]{8,}',
    '(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*',
    '(?i)(aws_access_key_id|aws_secret_access_key)\s*=\s*\S+',
    '-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
    'ghp_[a-zA-Z0-9]{36}',
    'gho_[a-zA-Z0-9]{36}'
)

# ── Logging ──────────────────────────────────────────────────
function Write-Log {
    param([string]$Level = "INFO", [string]$Message)
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
    $line = "$ts | $($Level.PadRight(8)) | CLONE-PS | $Message"
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
    switch ($Level) {
        "ERROR"   { Write-Host $line -ForegroundColor Red }
        "WARNING" { Write-Host $line -ForegroundColor Yellow }
        "INFO"    { Write-Host $line -ForegroundColor Cyan }
        default   { Write-Host $line }
    }
}

function Get-GitCloneDir {
    param([string]$Url)
    $parts = $Url.TrimEnd('/') -split '/'
    if ($parts.Count -ge 2) {
        $owner = $parts[-2]
        $repo = $parts[-1]
    } else {
        $owner = "unknown"; $repo = "unknown"
    }
    return Join-Path $ReposDir "${owner}__${repo}"
}

function Get-Sha256File {
    param([string]$FilePath)
    if (Test-Path $FilePath) {
        return (Get-FileHash -Path $FilePath -Algorithm SHA256).Hash.ToLower()
    }
    return ""
}

function Find-License {
    param([string]$RepoPath)
    $licenseNames = @("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE",
                      "LICENCE.md", "LICENCE.txt", "COPYING", "COPYING.md")
    foreach ($name in $licenseNames) {
        $lPath = Join-Path $RepoPath $name
        if (Test-Path $lPath) {
            $content = Get-Content -Path $lPath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
            if ($content) {
                $lc = $content.ToLower()
                if ($lc -match "mit license|permission is hereby granted") { return "MIT", $name }
                if ($lc -match "apache.*2\.0") { return "Apache-2.0", $name }
                if ($lc -match "bsd.*3.clause") { return "BSD-3-Clause", $name }
                if ($lc -match "bsd.*2.clause") { return "BSD-2-Clause", $name }
                if ($lc -match "gnu general public license.*3") { return "GPL-3.0", $name }
                if ($lc -match "gnu general public license.*2") { return "GPL-2.0", $name }
                if ($lc -match "isc license") { return "ISC", $name }
                if ($lc -match "mozilla public license") { return "MPL-2.0", $name }
                return "UNKNOWN", $name
            }
        }
    }
    return "NONE", ""
}

function Find-DependencyFiles {
    param([string]$RepoPath)
    $deps = @()
    $candidates = @("package.json", "requirements.txt", "setup.py", "setup.cfg",
                    "pyproject.toml", "Pipfile", "Cargo.toml", "go.mod",
                    "pom.xml", "build.gradle", "Gemfile", "composer.json")
    foreach ($name in $candidates) {
        if (Test-Path (Join-Path $RepoPath $name)) {
            $deps += $name
        }
    }
    return $deps
}

function Test-SecretsScan {
    param([string]$RepoPath)
    $findings = @()
    $skipDirs = @(".git", "node_modules", "__pycache__", ".venv", "venv")
    $skipExts = @(".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".ttf",
                  ".eot", ".svg", ".mp4", ".webm", ".zip", ".tar", ".gz",
                  ".jar", ".class", ".pyc", ".exe", ".dll", ".so", ".dylib")

    Get-ChildItem -Path $RepoPath -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        $file = $_
        $relPath = $file.FullName.Substring($RepoPath.Length).TrimStart('\')
        $dirParts = $relPath -split '\\'

        # Check skip dirs
        $shouldSkip = $false
        foreach ($skip in $skipDirs) {
            if ($dirParts -contains $skip) { $shouldSkip = $true; break }
        }
        if ($shouldSkip) { return }

        if ($skipExts -contains $file.Extension.ToLower()) { return }
        if ($file.Length -gt 1MB) { return }

        try {
            $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
            if (-not $content) { return }
            foreach ($pattern in $SecretPatterns) {
                if ($content -match $pattern) {
                    $findings += "MATCH in $relPath"
                    break
                }
            }
        } catch { }
    }

    return $findings
}

# ── Main ─────────────────────────────────────────────────────
Write-Log "INFO" ("=" * 60)
Write-Log "INFO" "Project Berunda — Repository Clone (PowerShell)"
Write-Log "INFO" "Mode: $(if ($DryRun) {'DRY-RUN'} else {'LIVE CLONE'})"
Write-Log "INFO" "Workspace: $WorkspaceRoot"
Write-Log "INFO" ("=" * 60)

$targets = $GitResources.Clone()
if ($ResourceId) {
    if ($targets.ContainsKey($ResourceId)) {
        $single = @{ $ResourceId = $targets[$ResourceId] }
        $targets = $single
    } else {
        Write-Log "WARNING" "Resource $ResourceId is not a git-cloneable resource"
        exit 0
    }
}

$stats = @{ success = 0; failed = 0; skipped = 0 }

foreach ($rid in $targets.Keys) {
    $info = $targets[$rid]
    $url = $info.url
    $name = $info.name
    $classification = $info.classification
    $cloneDir = Get-GitCloneDir $url

    Write-Log "INFO" "Processing [$rid] $name"

    # Already cloned?
    if ((Test-Path $cloneDir) -and -not $Force) {
        Write-Log "INFO" "[$rid] SKIP — already cloned: $cloneDir"
        $stats.skipped++
        continue
    }

    if ($DryRun) {
        Write-Log "INFO" "[$rid] DRY-RUN — would clone: $url"
        Write-Log "INFO" "         -> $cloneDir"
        $stats.skipped++
        continue
    }

    # Remove existing if Force
    if ((Test-Path $cloneDir) -and $Force) {
        Write-Log "WARNING" "[$rid] Force mode — removing existing clone"
        Remove-Item -Path $cloneDir -Recurse -Force -ErrorAction SilentlyContinue
    }

    # ── CLONE ──
    Write-Log "INFO" "[$rid] CLONING: $name | $url"
    New-Item -ItemType Directory -Path $ReposDir -Force | Out-Null

    $retries = 5
    $cloneSuccess = $false
    for ($attempt = 1; $attempt -le $retries; $attempt++) {
        Write-Log "INFO" "  Attempt $attempt/$retries"
        $gitOutput = git clone --depth 1 $url $cloneDir 2>&1
        if ($LASTEXITCODE -eq 0) {
            $cloneSuccess = $true
            break
        }
        Write-Log "WARNING" "  Attempt $attempt failed: $gitOutput"
        if ($attempt -lt $retries) {
            $backoff = [Math]::Pow(2, $attempt)
            Write-Log "INFO" "  Waiting ${backoff}s..."
            Start-Sleep -Seconds $backoff
        }
    }

    if (-not $cloneSuccess) {
        Write-Log "ERROR" "[$rid] Clone failed after $retries attempts"
        $stats.failed++
        continue
    }

    # Pin commit
    $pinnedCommit = git -C $cloneDir rev-parse HEAD 2>&1
    git -C $cloneDir tag "berunda-pin-$rid" HEAD 2>&1 | Out-Null
    Write-Log "INFO" "[$rid] Pinned at commit: $pinnedCommit"

    # License detection
    $spdx, $licenseFile = Find-License $cloneDir
    Write-Log "INFO" "[$rid] License: $spdx ($licenseFile)"

    # Dependency files
    $depFiles = Find-DependencyFiles $cloneDir
    if ($depFiles.Count -gt 0) {
        Write-Log "INFO" "[$rid] Dependency files: $($depFiles -join ', ')"
    }

    # Secrets scan
    Write-Log "INFO" "[$rid] Running secrets scan..."
    $findings = Test-SecretsScan $cloneDir
    $scanResult = if ($findings.Count -eq 0) { "CLEAN" } else { "ALERT: $($findings.Count) finding(s)" }
    if ($findings.Count -gt 0) {
        Write-Log "WARNING" "[$rid] Secrets scan: $scanResult"
        foreach ($f in $findings[0..[Math]::Min(9, $findings.Count-1)]) {
            Write-Log "WARNING" "  $f"
        }
    } else {
        Write-Log "INFO" "[$rid] Secrets scan: CLEAN"
    }

    # Write to repository_inventory.csv
    $csvPath = Join-Path $ManifestsDir "repository_inventory.csv"
    $csvHeader = "resource_id,repo_url,clone_path,pinned_commit,license_spdx,classification,dependency_file,secrets_scan_result"
    $csvLine = "$rid,$url,$(($cloneDir.Substring($WorkspaceRoot.Length)).TrimStart('\')),$pinnedCommit,$spdx,$classification,$($depFiles -join ';'),$scanResult"
    $csvExists = (Test-Path $csvPath) -and ((Get-Item $csvPath).Length -gt 0)

    if (-not $csvExists) {
        Set-Content -Path $csvPath -Value $csvHeader -Encoding UTF8
    }
    Add-Content -Path $csvPath -Value $csvLine -Encoding UTF8

    Write-Log "INFO" "[$rid] SUCCESS — cloned, pinned, scanned"
    $stats.success++
}

# Summary
$exitCode = if ($stats.failed -gt 0 -and $stats.success -gt 0) { 1 } elseif ($stats.failed -gt 0) { 2 } else { 0 }

Write-Log "INFO" ("=" * 60)
Write-Log "INFO" "CLONE SUMMARY (PowerShell)"
Write-Log "INFO" "  Success:  $($stats.success)"
Write-Log "INFO" "  Skipped:  $($stats.skipped)"
Write-Log "INFO" "  Failed:   $($stats.failed)"
Write-Log "INFO" ("=" * 60)

exit $exitCode
