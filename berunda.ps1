<#
.SYNOPSIS
    Berunda Build Orchestration Script
.DESCRIPTION
    Centralized PowerShell script for building, testing, linting, and deploying
    the Berunda crime intelligence platform.
.PARAMETER WhatIf
    Show what would be done without executing.
.EXAMPLE
    ./berunda.ps1 setup
    ./berunda.ps1 test -WhatIf
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet("setup", "build", "test", "lint", "clean", "docker-build", "docker-up", "docker-down", "help")]
    [string]$Command = "help",

    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

function Invoke-Native {
    param([string]$Command, [string]$Arguments)
    if ($WhatIf) {
        Write-Log "[WHATIF] Would execute: $Command $Arguments" -Level "WHATIF"
        return
    }
    Write-Log "Executing: $Command $Arguments"
    $exitCode = 0
    try {
        & $Command $Arguments
        if (-not $?) { $exitCode = 1 }
    } catch {
        Write-Log "Command failed: $_" -Level "ERROR"
        $exitCode = 1
    }
    if ($exitCode -ne 0) {
        throw "Command failed with exit code $exitCode: $Command $Arguments"
    }
}

function Invoke-Setup {
    Write-Log "=== Setup: Installing dependencies ==="

    # Python dependencies
    if (Get-Command python -ErrorAction SilentlyContinue) {
        Write-Log "Installing Python dependencies..."
        Invoke-Native "pip" "install -r requirements.txt"
    } else {
        Write-Log "Python not found. Skipping Python deps." -Level "WARN"
    }

    # Node dependencies
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        Write-Log "Installing root Node dependencies..."
        Invoke-Native "npm" "install"

        if (Test-Path (Join-Path $ROOT "apps\web")) {
            Write-Log "Installing web app dependencies..."
            Push-Location (Join-Path $ROOT "apps\web")
            Invoke-Native "npm" "install"
            Pop-Location
        }

        if (Test-Path (Join-Path $ROOT "apps\api")) {
            Write-Log "Installing API dependencies..."
            Push-Location (Join-Path $ROOT "apps\api")
            Invoke-Native "npm" "install"
            Pop-Location
        }
    } else {
        Write-Log "npm not found. Skipping Node deps." -Level "WARN"
    }

    # Catalyst CLI
    if (Get-Command catalyst -ErrorAction SilentlyContinue) {
        Write-Log "Catalyst CLI detected."
    } else {
        Write-Log "Catalyst CLI not found. Install from: https://help.catalyst.zoho.com" -Level "WARN"
    }

    Write-Log "Setup complete."
}

function Invoke-Build {
    Write-Log "=== Build: Building applications ==="

    # Build web app
    $webPath = Join-Path $ROOT "apps\web"
    if (Test-Path $webPath) {
        Write-Log "Building web app..."
        Push-Location $webPath
        Invoke-Native "npm" "run build"
        Pop-Location
        Write-Log "Web app build complete."
    }

    Write-Log "Build complete."
}

function Invoke-Test {
    param([string]$Category = "all")
    Write-Log "=== Test: Running tests ($Category) ==="

    # Python tests
    if (Get-Command pytest -ErrorAction SilentlyContinue) {
        $pytestArgs = @()
        switch ($Category) {
            "unit" { $pytestArgs += "-m unit" }
            "integration" { $pytestArgs += "-m integration" }
            "all" { }
            default { $pytestArgs += "-m $Category" }
        }
        $pytestArgs += "--tb=short"
        $pytestArgs += "--cov=src"
        $pytestArgs += "--cov-report=term-missing"

        Write-Log "Running pytest with args: $($pytestArgs -join ' ')"
        Invoke-Native "pytest" $pytestArgs
    } else {
        Write-Log "pytest not found. Skipping Python tests." -Level "WARN"
    }

    # Frontend tests
    $webPath = Join-Path $ROOT "apps\web"
    if (Test-Path $webPath) {
        Write-Log "Running web app tests..."
        Push-Location $webPath
        Invoke-Native "npm" "run test"
        Pop-Location
    }

    Write-Log "Tests complete."
}

function Invoke-Lint {
    Write-Log "=== Lint: Checking code quality ==="

    # Python linting
    if (Get-Command ruff -ErrorAction SilentlyContinue) {
        Write-Log "Running ruff..."
        Invoke-Native "ruff" "check src/ apps/ tests/"
        Invoke-Native "ruff" "format --check src/ apps/ tests/"
    } else {
        Write-Log "ruff not found. Try: pip install ruff" -Level "WARN"
    }

    if (Get-Command mypy -ErrorAction SilentlyContinue) {
        Write-Log "Running mypy..."
        Invoke-Native "mypy" "src/ --ignore-missing-imports"
    } else {
        Write-Log "mypy not found. Try: pip install mypy" -Level "WARN"
    }

    # Frontend linting
    $webPath = Join-Path $ROOT "apps\web"
    if (Test-Path $webPath -and (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Log "Running ESLint..."
        Push-Location $webPath
        Invoke-Native "npm" "run lint"
        Pop-Location
    }

    Write-Log "Lint complete."
}

function Invoke-Clean {
    Write-Log "=== Clean: Removing build artifacts ==="

    $patterns = @(
        "**/__pycache__",
        "**/.pytest_cache",
        "**/.ruff_cache",
        "**/.mypy_cache",
        "**/node_modules",
        "**/dist",
        "**/build",
        "**/*.egg-info",
        "**/.coverage",
        "**/coverage"
    )

    foreach ($pattern in $patterns) {
        $items = Get-ChildItem -Path $ROOT -Directory -Filter $pattern -Recurse -ErrorAction SilentlyContinue
        foreach ($item in $items) {
            if ($WhatIf) {
                Write-Log "[WHATIF] Would remove: $($item.FullName)" -Level "WHATIF"
            } else {
                Remove-Item -Path $item.FullName -Recurse -Force -ErrorAction SilentlyContinue
                Write-Log "Removed: $($item.FullName)"
            }
        }
    }

    Write-Log "Clean complete."
}

function Invoke-DockerBuild {
    Write-Log "=== Docker: Building images ==="
    $composeFile = Join-Path $ROOT "docker-compose.yml"
    if (Test-Path $composeFile) {
        Invoke-Native "docker-compose" "-f $composeFile build"
    } else {
        Write-Log "docker-compose.yml not found." -Level "ERROR"
    }
    Write-Log "Docker build complete."
}

function Invoke-DockerUp {
    Write-Log "=== Docker: Starting services ==="
    $composeFile = Join-Path $ROOT "docker-compose.yml"
    if (Test-Path $composeFile) {
        Invoke-Native "docker-compose" "-f $composeFile up -d"
        Write-Log "Services started. Use 'docker-compose ps' to check status."
    } else {
        Write-Log "docker-compose.yml not found." -Level "ERROR"
    }
}

function Invoke-DockerDown {
    Write-Log "=== Docker: Stopping services ==="
    $composeFile = Join-Path $ROOT "docker-compose.yml"
    if (Test-Path $composeFile) {
        Invoke-Native "docker-compose" "-f $composeFile down"
    } else {
        Write-Log "docker-compose.yml not found." -Level "ERROR"
    }
}

function Show-Help {
    Write-Host @"
Berunda Build Orchestration Script
===================================

Usage:
  .\berunda.ps1 <command> [-WhatIf]

Commands:
  setup         Install all dependencies (pip, npm)
  build         Build all applications
  test          Run all tests
  lint          Run linters and type checkers
  clean         Remove build artifacts
  docker-build  Build Docker images
  docker-up     Start Docker Compose services
  docker-down   Stop Docker Compose services
  help          Show this help message

Options:
  -WhatIf       Show what would be done without executing

Examples:
  .\berunda.ps1 setup
  .\berunda.ps1 test
  .\berunda.ps1 docker-build -WhatIf
"@
}

# ── Dispatch ─────────────────────────────────────────────────
switch ($Command) {
    "setup" { Invoke-Setup }
    "build" { Invoke-Build }
    "test" { Invoke-Test }
    "lint" { Invoke-Lint }
    "clean" { Invoke-Clean }
    "docker-build" { Invoke-DockerBuild }
    "docker-up" { Invoke-DockerUp }
    "docker-down" { Invoke-DockerDown }
    "help" { Show-Help }
    default { Show-Help }
}
