# ============================================================
# download_resources.ps1 — Resource Acquisition (PowerShell)
# Project Berunda — Karnataka State Police Datathon 2026
#
# Downloads resources into quarantine/ following safety rules.
# Validates and moves to data/raw/ on success.
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

# ── Paths ────────────────────────────────────────────────────
$QuarantineDir = Join-Path $WorkspaceRoot "quarantine"
$RawDir = Join-Path $WorkspaceRoot "data" "raw"
$ManifestsDir = Join-Path $WorkspaceRoot "manifests"
$LogFile = Join-Path $WorkspaceRoot "logs" "acquisition.log"
$ManifestJson = Join-Path $ManifestsDir "resource_manifest.json"

# ── Domain allowlist (from AGENTS.md) ────────────────────────
$DomainAllowlist = @(
    "hack2skill.com", "catalyst.zoho.com", "help.catalyst.zoho.com",
    "ncrb.gov.in", "data.gov.in", "ksp.karnataka.gov.in",
    "ndap.niti.gov.in", "overpass-api.de", "bhuvan.nrsc.gov.in",
    "censusindia.gov.in", "open-meteo.com", "indiacode.nic.in",
    "bprd.nic.in", "github.com", "js.cytoscape.org", "pypi.org",
    "npmjs.com", "owasp.org", "nist.gov", "geojson.org",
    "networkx.org", "neo4j.com"
)

$SkipMethods = @{
    "MANUAL-AUTHORIZED"              = "Requires human action"
    "AUTO-BROWSER-WITH-USER-SESSION" = "Requires authenticated browser session"
    "SEMI-AUTOMATED"                 = "Requires human confirmation"
    "DO-NOT-ACQUIRE"                 = "Explicitly excluded"
    "FUTURE-RESTRICTED"              = "Not acquired under this blueprint"
    "AUTO-API"                       = "Use dedicated API scripts"
    "AUTO-GIT"                       = "Use clone_repositories scripts"
}

# ── Retry config ─────────────────────────────────────────────
$MaxRetries = 5
$BackoffBase = 2
$ConnectTimeoutSec = 30
$DownloadTimeoutSec = 300

# ── Logging ──────────────────────────────────────────────────
function Write-Log {
    param([string]$Level = "INFO", [string]$Message)
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
    $line = "$ts | $($Level.PadRight(8)) | DOWNLOAD-PS | $Message"
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
    switch ($Level) {
        "ERROR"   { Write-Host $line -ForegroundColor Red }
        "WARNING" { Write-Host $line -ForegroundColor Yellow }
        "INFO"    { Write-Host $line -ForegroundColor Cyan }
        default   { Write-Host $line }
    }
}

function Get-Sha256 {
    param([string]$FilePath)
    return (Get-FileHash -Path $FilePath -Algorithm SHA256).Hash.ToLower()
}

function Test-DomainAllowed {
    param([string]$Url)
    try {
        $uri = [System.Uri]::new($Url)
        $host_ = $uri.Host
        foreach ($d in $DomainAllowlist) {
            if ($host_ -eq $d -or $host_.EndsWith(".$d")) { return $true }
        }
        return $false
    } catch {
        return $false
    }
}

function Test-PathInWorkspace {
    param([string]$Path)
    try {
        $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop
        return $resolved.Path.StartsWith($WorkspaceRoot)
    } catch {
        $parent = Split-Path $Path -Parent
        if ($parent -and (Test-Path $parent)) {
            $resolved = (Resolve-Path -LiteralPath $parent).Path
            return $resolved.StartsWith($WorkspaceRoot)
        }
        return $false
    }
}

# ── Main ─────────────────────────────────────────────────────
Write-Log "INFO" ("=" * 60)
Write-Log "INFO" "Project Berunda — Resource Acquisition (PowerShell)"
Write-Log "INFO" "Mode: $(if ($DryRun) {'DRY-RUN'} else {'LIVE DOWNLOAD'})"
Write-Log "INFO" "Workspace: $WorkspaceRoot"
Write-Log "INFO" ("=" * 60)

# Load manifest
if (-not (Test-Path $ManifestJson)) {
    Write-Log "ERROR" "Manifest not found: $ManifestJson"
    exit 2
}

$resources = Get-Content $ManifestJson -Raw | ConvertFrom-Json

# Apply filters
if ($ResourceId) { $resources = $resources | Where-Object { $_.rsrc_id -eq $ResourceId } }
if ($Priority)  { $resources = $resources | Where-Object { $_.priority -eq $Priority } }

Write-Log "INFO" "Processing $($resources.Count) resource(s)"

$stats = @{ downloaded = 0; skipped = 0; failed = 0; dryrun = 0 }
$totalBytes = 0

foreach ($r in $resources) {
    $rid    = $r.rsrc_id
    $method = $r.method
    $url    = $r.source_url
    $status = $r.status
    $name   = $r.name

    # Already completed
    if ($status -eq "completed" -and -not $Force) {
        Write-Log "INFO" "[$rid] SKIP — already completed: $name"
        $stats.skipped++
        continue
    }

    # Skip by method
    if ($SkipMethods.ContainsKey($method)) {
        Write-Log "INFO" "[$rid] SKIP — $($SkipMethods[$method]): $name"
        $stats.skipped++
        continue
    }

    if ($method -match "pip|npm") {
        Write-Log "INFO" "[$rid] SKIP — package manager install: $name"
        $stats.skipped++
        continue
    }

    if ($method -ne "AUTO-DIRECT-DOWNLOAD") {
        Write-Log "INFO" "[$rid] SKIP — method '$method' not handled: $name"
        $stats.skipped++
        continue
    }

    if (-not $url -or $url -in @("n/a", "various", "organizer Resources tab", "UNVERIFIED")) {
        Write-Log "WARNING" "[$rid] SKIP — no valid URL: $url"
        $stats.skipped++
        continue
    }

    if (-not (Test-DomainAllowed $url)) {
        Write-Log "WARNING" "[$rid] BLOCKED — domain not on allowlist: $url"
        $stats.skipped++
        continue
    }

    if ($totalBytes -ge $MaxTotalSize) {
        Write-Log "WARNING" "[$rid] BLOCKED — total download limit ($MaxTotalSize bytes) reached"
        $stats.skipped++
        continue
    }

    # Destination path
    $dateSuffix = Get-Date -Format "yyyyMMdd"
    try {
        $uriObj = [System.Uri]::new($url)
        $urlFilename = [System.IO.Path]::GetFileName($uriObj.LocalPath)
    } catch { $urlFilename = "" }
    if (-not $urlFilename -or $urlFilename -eq "/") { $urlFilename = "${rid}_resource" }

    $stem = [System.IO.Path]::GetFileNameWithoutExtension($urlFilename)
    $ext  = [System.IO.Path]::GetExtension($urlFilename)
    if (-not $ext) { $ext = ".html" }
    $destFilename = "${stem}_${dateSuffix}${ext}"
    $destDir = Join-Path $QuarantineDir $rid
    $destPath = Join-Path $destDir $destFilename

    if (-not (Test-PathInWorkspace $destPath)) {
        Write-Log "ERROR" "[$rid] SECURITY — path escapes workspace: $destPath"
        $stats.failed++
        continue
    }

    # Idempotency
    if ((Test-Path $destPath) -and -not $Force) {
        $existingHash = Get-Sha256 $destPath
        Write-Log "INFO" "[$rid] SKIP — already in quarantine: $destFilename ($($existingHash.Substring(0,16))...)"
        $stats.skipped++
        continue
    }

    # Dry run
    if ($DryRun) {
        Write-Log "INFO" "[$rid] DRY-RUN — would download: $url"
        Write-Log "INFO" "         -> $destPath"
        $stats.dryrun++
        continue
    }

    # ── ACTUAL DOWNLOAD with retry & backoff ──
    Write-Log "INFO" "[$rid] DOWNLOADING: $name | $url"
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null

    $success = $false
    $httpStatus = 0
    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
        try {
            Write-Log "INFO" "  Attempt $attempt/$MaxRetries"

            $iwrParams = @{
                Uri              = $url
                OutFile          = $destPath
                Headers          = @{ "User-Agent" = "ProjectBerunda-AcquisitionAgent/1.0" }
                UseBasicParsing  = $true
                ErrorAction      = "Stop"
                TimeoutSec       = $DownloadTimeoutSec
            }
            if ($Resume -and (Test-Path $destPath)) {
                $existingSize = (Get-Item $destPath).Length
                $iwrParams.Headers["Range"] = "bytes=$existingSize-"
            }

            Invoke-WebRequest @iwrParams 2>&1 | Out-Null
            $success = $true
            break
        } catch {
            if ($_.Exception.Response) {
                $httpStatus = [int]$_.Exception.Response.StatusCode
            }
            Write-Log "WARNING" "  Attempt $attempt failed (HTTP $httpStatus): $($_.Exception.Message)"

            if ($httpStatus -ge 400 -and $httpStatus -lt 500 -and $httpStatus -ne 429) {
                Write-Log "WARNING" "  Non-retryable HTTP error — skipping"
                break
            }

            if ($attempt -lt $MaxRetries) {
                $backoff = [Math]::Pow($BackoffBase, $attempt)
                Write-Log "INFO" "  Waiting ${backoff}s before retry..."
                Start-Sleep -Seconds $backoff
            }
        }
    }

    if (-not $success) {
        Write-Log "ERROR" "[$rid] FAILED — all $MaxRetries attempts exhausted"
        $stats.failed++
        continue
    }

    # Post-download validation
    $fileSize = (Get-Item $destPath).Length
    if ($fileSize -gt $MaxFileSize) {
        Write-Log "WARNING" "[$rid] File exceeds max size ($fileSize > $MaxFileSize) — requires approval, removing"
        Remove-Item $destPath -Force -ErrorAction SilentlyContinue
        $stats.failed++
        continue
    }

    $checksum = Get-Sha256 $destPath
    $shaFile = "$destPath.sha256"
    Set-Content -Path $shaFile -Value "$checksum  $destFilename" -Encoding UTF8
    $totalBytes += $fileSize
    $stats.downloaded++

    Write-Log "INFO" "[$rid] SUCCESS — $fileSize bytes, sha256: $checksum"

    # Move validated file from quarantine to data/raw/
    $rawDestDir = Join-Path $RawDir $rid
    New-Item -ItemType Directory -Path $rawDestDir -Force | Out-Null
    $rawDestPath = Join-Path $rawDestDir $destFilename

    if (Test-Path $rawDestPath) {
        Remove-Item $rawDestPath -Force -ErrorAction SilentlyContinue
    }
    Move-Item -Path $destPath -Destination $rawDestPath -Force
    Move-Item -Path $shaFile -Destination "$rawDestPath.sha256" -Force
    Write-Log "INFO" "[$rid] PROMOTED to: $rawDestPath"

    # Update download manifest
    $csvLine = "$rid,$url,200,$fileSize,$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ'),$("." + $rawDestPath.Substring($WorkspaceRoot.Length)),$checksum"
    Add-Content -Path (Join-Path $ManifestsDir "download_manifest.csv") -Value $csvLine -Encoding UTF8
}

# Summary
$exitCode = if ($stats.failed -gt 0 -and $stats.downloaded -gt 0) { 1 } elseif ($stats.failed -gt 0) { 2 } else { 0 }

Write-Log "INFO" ("=" * 60)
Write-Log "INFO" "ACQUISITION SUMMARY (PowerShell)"
Write-Log "INFO" "  Downloaded:  $($stats.downloaded)"
Write-Log "INFO" "  Skipped:     $($stats.skipped)"
Write-Log "INFO" "  Failed:      $($stats.failed)"
Write-Log "INFO" "  Dry-run:     $($stats.dryrun)"
Write-Log "INFO" "  Total bytes: $totalBytes"
Write-Log "INFO" ("=" * 60)
Write-Log "INFO" "Exit code: $exitCode"

exit $exitCode
