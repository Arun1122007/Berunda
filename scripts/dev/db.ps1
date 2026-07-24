param(
    [ValidateSet("migrate", "rollback", "seed", "history", "current", "reset")]
    [string]$Command = "migrate",
    [string]$Revision = "head",
    [switch]$WhatIf
)

$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$env:APP_ENV = "development"

switch ($Command) {
    "migrate" {
        Write-Host "Running migrations up to $Revision ..." -ForegroundColor Cyan
        if (-not $WhatIf) { alembic -c "$ROOT\src\alembic.ini" upgrade $Revision }
    }
    "rollback" {
        Write-Host "Rolling back to $Revision ..." -ForegroundColor Yellow
        if (-not $WhatIf) { alembic -c "$ROOT\src\alembic.ini" downgrade $Revision }
    }
    "seed" {
        Write-Host "Loading demo seed data..." -ForegroundColor Cyan
        if (-not $WhatIf) { python -m scripts.data.seed_demo }
    }
    "history" {
        if (-not $WhatIf) { alembic -c "$ROOT\src\alembic.ini" history }
    }
    "current" {
        if (-not $WhatIf) { alembic -c "$ROOT\src\alembic.ini" current }
    }
    "reset" {
        Write-Host "Resetting database..." -ForegroundColor Yellow
        $db = "$ROOT\berunda.db"
        $devDb = "$ROOT\data\berunda_dev.db"
        if (Test-Path $db) { Remove-Item $db -Force; Write-Host "  Removed $db" }
        if (Test-Path $devDb) { Remove-Item $devDb -Force; Write-Host "  Removed $devDb" }
        Write-Host "Running fresh migrations..."
        if (-not $WhatIf) { alembic -c "$ROOT\src\alembic.ini" upgrade head }
        Write-Host "Loading seed data..."
        if (-not $WhatIf) { python -m scripts.data.seed_demo }
        Write-Host "Database reset complete."
    }
}
