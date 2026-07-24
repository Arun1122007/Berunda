param(
    [ValidateSet("build", "up", "down", "logs", "rebuild", "status")]
    [string]$Command = "status",
    [switch]$WhatIf
)

$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$COMPOSE = "$ROOT\docker-compose.yml"

if (-not (Test-Path $COMPOSE)) {
    Write-Error "docker-compose.yml not found at $COMPOSE"
    exit 1
}

switch ($Command) {
    "build" {
        Write-Host "Building Docker images..." -ForegroundColor Cyan
        if (-not $WhatIf) { docker-compose -f $COMPOSE build }
    }
    "up" {
        Write-Host "Starting all services..." -ForegroundColor Cyan
        if (-not $WhatIf) { docker-compose -f $COMPOSE up -d }
        Write-Host "Services:"
        Write-Host "  API:      http://localhost:9000"
        Write-Host "  Frontend: http://localhost:5173"
        Write-Host "  Grafana:  http://localhost:3000 (admin/admin)"
        Write-Host "  Prometheus: http://localhost:9090"
    }
    "down" {
        Write-Host "Stopping all services..." -ForegroundColor Cyan
        if (-not $WhatIf) { docker-compose -f $COMPOSE down }
    }
    "logs" {
        if (-not $WhatIf) { docker-compose -f $COMPOSE logs -f }
    }
    "rebuild" {
        Write-Host "Rebuilding and restarting..." -ForegroundColor Cyan
        if (-not $WhatIf) {
            docker-compose -f $COMPOSE down
            docker-compose -f $COMPOSE build
            docker-compose -f $COMPOSE up -d
        }
    }
    "status" {
        if (-not $WhatIf) { docker-compose -f $COMPOSE ps }
    }
}
