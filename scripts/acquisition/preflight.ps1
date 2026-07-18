# ============================================================
# preflight.ps1 — Phase 0 Preflight Check
# Project Berunda Resource Acquisition
# Produces: reports/PREFLIGHT_REPORT.md & git checkpoint
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

$ErrorActionPreference = "Stop"
$exitCode = 0
$reportPath = Join-Path $WorkspaceRoot "reports" "PREFLIGHT_REPORT.md"
$logFile = Join-Path $WorkspaceRoot "logs" "acquisition.log"

function Write-Log {
    param([string]$Level = "INFO", [string]$Message)
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
    $line = "$ts | $($Level.PadRight(8)) | PREFLIGHT | $Message"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    switch ($Level) {
        "ERROR"   { Write-Host $line -ForegroundColor Red }
        "WARNING" { Write-Host $line -ForegroundColor Yellow }
        "INFO"    { Write-Host $line -ForegroundColor Cyan }
        default   { Write-Host $line }
    }
}

function Get-ToolVersion {
    param([string]$Command, [string]$Args)
    try {
        $output = & $Command $Args 2>&1 | Out-String
        return $output.Trim()
    } catch {
        return "NOT FOUND"
    }
}

function Test-RequiredDirectories {
    param([string[]]$Dirs)
    $missing = @()
    foreach ($d in $Dirs) {
        $fullPath = Join-Path $WorkspaceRoot $d
        if (-not (Test-Path $fullPath)) {
            $missing += $d
        }
    }
    return $missing
}

# ============================================================
Write-Log "INFO" ("=" * 60)
Write-Log "INFO" "Project Berunda — Phase 0 Preflight"
Write-Log "INFO" "Workspace root: $WorkspaceRoot"
Write-Log "INFO" ("=" * 60)

# Validate workspace is a git repo
if (-not (Test-Path (Join-Path $WorkspaceRoot ".git"))) {
    Write-Log "ERROR" "No .git directory found at workspace root"
    exit 2
}

# ============================================================
# 1. Environment detection
# ============================================================
Write-Log "INFO" "Detecting environment..."

$envInfo = [ordered]@{
    "OS"          = [System.Environment]::OSVersion.VersionString
    "PowerShell"  = $PSVersionTable.PSVersion.ToString()
    "Python"      = Get-ToolVersion "python" "--version"
    "Git"         = Get-ToolVersion "git" "--version"
    "Node"        = Get-ToolVersion "node" "--version"
    "pip"         = Get-ToolVersion "pip" "--version"
}

foreach ($k in $envInfo.Keys) {
    Write-Log "INFO" "  $k = $($envInfo[$k])"
}

# ============================================================
# 2. Disk space check (halt if < 10 GB)
# ============================================================
Write-Log "INFO" "Checking disk space..."
$drive = (Get-Item $WorkspaceRoot).PSDrive
$freeGB = [math]::Round($drive.Free / 1GB, 2)
$usedGB = [math]::Round($drive.Used / 1GB, 2)
$totalGB = [math]::Round(($drive.Free + $drive.Used) / 1GB, 2)
Write-Log "INFO" "  Drive $($drive.Name): $freeGB GB free / $totalGB GB total"

if ($freeGB -lt 10) {
    Write-Log "ERROR" "Insufficient disk space: ${freeGB}GB free (< 10 GB required) — halting"
    $exitCode = 2
    # Continue to generate partial report
}

# ============================================================
# 3. Required directories
# ============================================================
$requiredDirs = @("data", "data/raw", "quarantine", "repositories", "manifests",
                   "logs", "reports", "config", "scripts/acquisition", "scripts/validation")
$missingDirs = Test-RequiredDirectories $requiredDirs

if ($missingDirs.Count -gt 0) {
    Write-Log "WARNING" "Missing directories: $($missingDirs -join ', ')"
    if (-not $DryRun) {
        foreach ($d in $missingDirs) {
            $fullPath = Join-Path $WorkspaceRoot $d
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            Write-Log "INFO" "  Created: $d"
        }
    } else {
        Write-Log "INFO" "  (dry-run — would create $($missingDirs.Count) missing directories)"
    }
} else {
    Write-Log "INFO" "All required directories exist"
}

# ============================================================
# 4. Domain allowlist (from AGENTS.md)
# ============================================================
$domainAllowlist = @(
    "hack2skill.com", "catalyst.zoho.com", "help.catalyst.zoho.com",
    "ncrb.gov.in", "data.gov.in", "ksp.karnataka.gov.in",
    "ndap.niti.gov.in", "overpass-api.de", "bhuvan.nrsc.gov.in",
    "censusindia.gov.in", "open-meteo.com", "indiacode.nic.in",
    "bprd.nic.in", "github.com", "js.cytoscape.org", "pypi.org",
    "npmjs.com", "owasp.org", "nist.gov"
)

Write-Log "INFO" "Domain allowlist: $($domainAllowlist.Count) domains registered"

# ============================================================
# 5. File inventory
# ============================================================
$dataDirs = @("data", "resources", "repositories", "boundaries", "quarantine", "models")
$existingFiles = @()
foreach ($dir in $dataDirs) {
    $fullDir = Join-Path $WorkspaceRoot $dir
    if (Test-Path $fullDir) {
        $files = Get-ChildItem -Path $fullDir -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -ne ".gitkeep" }
        foreach ($f in $files) {
            $existingFiles += [PSCustomObject]@{
                Path = $f.FullName.Replace($WorkspaceRoot, ".")
                Size = $f.Length
                LastModified = $f.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
            }
        }
    }
}
Write-Log "INFO" "Existing data/resource files: $($existingFiles.Count)"

# ============================================================
# 6. Git state and checkpoint
# ============================================================
$gitBranch = git -C $WorkspaceRoot rev-parse --abbrev-ref HEAD 2>&1
$gitCommit = git -C $WorkspaceRoot rev-parse --short HEAD 2>&1
$gitRemote = git -C $WorkspaceRoot remote get-url origin 2>&1
$gitDirty = git -C $WorkspaceRoot status --porcelain 2>&1

Write-Log "INFO" "Git: branch=$gitBranch commit=$gitCommit"

if (-not $DryRun) {
    $checkpointTag = "preflight-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    git -C $WorkspaceRoot tag -f $checkpointTag HEAD 2>&1 | Out-Null
    Write-Log "INFO" "Git checkpoint tag created: $checkpointTag"
} else {
    Write-Log "INFO" "(dry-run — would create git checkpoint tag)"
}

# ============================================================
# 7. Python packages
# ============================================================
$pipList = pip list --format=json 2>&1 | ConvertFrom-Json -ErrorAction SilentlyContinue
$relevantPackages = @("Faker", "networkx", "pandas", "requests", "shapely", "geopandas", "GitPython")
$installedPackages = @()
$missingPackages = @()

foreach ($pkg in $relevantPackages) {
    $found = $pipList | Where-Object { $_.name -eq $pkg }
    if ($found) {
        $installedPackages += "$pkg==$($found.version)"
    } else {
        $missingPackages += $pkg
    }
}

# ============================================================
# 8. Manifest state
# ============================================================
$manifestDir = Join-Path $WorkspaceRoot "manifests"
$manifestFiles = @()
if (Test-Path $manifestDir) {
    $manifestFiles = Get-ChildItem -Path $manifestDir -File | Select-Object Name, Length
}

# ============================================================
# 9. Generate report
# ============================================================
$diskWarning = ""
if ($freeGB -lt 10) {
    $diskWarning = "> [!CAUTION]`n> Disk space CRITICAL: ${freeGB}GB free (< 10 GB). Halting acquisition.`n"
} elseif ($freeGB -lt 20) {
    $diskWarning = "> [!WARNING]`n> Disk space low: ${freeGB}GB free. Monitor during acquisition.`n"
}

$existingTable = ""
if ($existingFiles.Count -eq 0) {
    $existingTable = "No existing data/resource files found.`n"
} else {
    $existingTable = "| Path | Size (bytes) | Last Modified |`n|------|-------------|---------------|`n"
    foreach ($f in $existingFiles) {
        $existingTable += "| $($f.Path) | $($f.Size) | $($f.LastModified) |`n"
    }
}

$manifestTable = ""
if ($manifestFiles.Count -eq 0) {
    $manifestTable = "No manifest files found.`n"
} else {
    $manifestTable = "| File | Size (bytes) |`n|------|-------------|`n"
    foreach ($m in $manifestFiles) {
        $manifestTable += "| $($m.Name) | $($m.Length) |`n"
    }
}

$pipSection = ""
if ($missingPackages.Count -gt 0) {
    $pipSection = "**Missing:** $($missingPackages -join ', ')`n`n"
    $pipSection += "``````bash`npip install $($missingPackages -join ' ')`n```````n"
} else {
    $pipSection = "All recommended packages are installed.`n"
}

$report = @"
# Preflight Report

> **Generated:** $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssK")
> **Workspace:** $WorkspaceRoot
> **Status:** $(if ($exitCode -eq 2) { "FAILED — disk space critical" } else { "COMPLETE" })

---
## 1. Environment

| Tool | Version |
|------|---------|
$(foreach ($k in $envInfo.Keys) { "| $k | $($envInfo[$k]) |`n" })

## 2. Disk Space

| Drive | Free (GB) | Used (GB) | Total (GB) |
|-------|-----------|-----------|------------|
| $($drive.Name): | $freeGB | $usedGB | $totalGB |

$diskWarning
## 3. Git State

| Field | Value |
|-------|-------|
| Branch | $gitBranch |
| Commit | $gitCommit |
| Remote | $gitRemote |
| Dirty | $(if ($gitDirty) { "Yes — $($gitDirty.Count) file(s)" } else { "Clean" }) |

## 4. Existing Data Files

$existingTable
## 5. Python Packages

**Installed:** $($installedPackages -join ", ")

$pipSection
## 6. Manifest Files

$manifestTable
## 7. Domain Allowlist ($($domainAllowlist.Count) domains)

$(foreach ($d in $domainAllowlist) { "- ``$d```n" })

## 8. Required Directories

| Directory | Status |
|-----------|--------|
$(foreach ($d in $requiredDirs) {
    $status = if ($d -in $missingDirs) { "MISSING" } else { "OK" }
    "| $d | $status |`n"
})

## 9. Recommendations

1. $(if ($missingPackages.Count -gt 0) { "Run ``pip install $($missingPackages -join ' ')``" } else { "All Python packages installed" })
2. Ensure all missing directories are created before acquisition
3. Verify domain allowlist covers all target resources
4. Manually confirm Hack2Skill dashboard access for R002

---
*End of Preflight Report*
"@

New-Item -ItemType Directory -Path (Split-Path $reportPath) -Force | Out-Null
Set-Content -Path $reportPath -Value $report -Encoding UTF8

Write-Log "INFO" "Preflight report written to $reportPath"

# ============================================================
# Summary
# ============================================================
Write-Host "`n============================================"
Write-Host "PREFLIGHT COMPLETE"
Write-Host "Report: $reportPath"
if ($exitCode -eq 2) { Write-Host "STATUS: FAILED — see report for details" -ForegroundColor Red }
else { Write-Host "STATUS: PASSED" -ForegroundColor Green }
Write-Host "============================================"

exit $exitCode
