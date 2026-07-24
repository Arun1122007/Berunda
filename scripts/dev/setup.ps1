param([switch]$WhatIf)
$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

function Write-Step { Write-Host "`n>>> $($args[0])" -ForegroundColor Cyan }

if ($WhatIf) { Write-Step "WHATIF mode — no changes will be made" }

Write-Step "Setting up Berunda development environment..."

Write-Step "1. Creating .env from .env.example..."
if (-not (Test-Path "$ROOT\.env")) {
    if (-not $WhatIf) { Copy-Item "$ROOT\.env.example" "$ROOT\.env" }
    Write-Step "   .env created"
} else {
    Write-Step "   .env already exists — skipping"
}

Write-Step "2. Installing Python dependencies..."
if (-not $WhatIf) {
    pushd $ROOT; pip install -r requirements.txt; popd
}

Write-Step "3. Installing web frontend dependencies..."
$webPath = "$ROOT\apps\web"
if (Test-Path $webPath) {
    if (-not $WhatIf) {
        pushd $webPath; npm install; popd
    }
}

Write-Step "Setup complete! Run '.\scripts\dev\dev.ps1' to start the dev servers."
