param(
    [ValidateSet("backend", "frontend", "all")]
    [string]$Service = "all"
)

$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

function Write-Step { Write-Host $args[0] -ForegroundColor Cyan }

if ($Service -eq "all" -or $Service -eq "backend") {
    Write-Step "Starting backend API on http://localhost:8000 ..."
    Start-Process -NoNewWindow powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT'; uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
}

if ($Service -eq "all" -or $Service -eq "frontend") {
    Write-Step "Starting frontend dev server on http://localhost:5173 ..."
    Start-Process -NoNewWindow powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT\apps\web'; npm run dev"
}

Write-Step "Dev servers starting..."
Write-Step "   Backend: http://localhost:8000"
Write-Step "   Frontend: http://localhost:5173"
Write-Step "   API docs: http://localhost:8000/docs"
