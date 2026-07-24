param(
    [ValidateSet("all", "unit", "integration", "lint", "typecheck")]
    [string]$Scope = "all",
    [switch]$WhatIf
)

$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

function Write-Step { Write-Host $args[0] -ForegroundColor Cyan }

if ($Scope -eq "all" -or $Scope -eq "lint") {
    Write-Step "=== Running ruff linter ==="
    if (-not $WhatIf) { ruff check "$ROOT\src\" "$ROOT\tests\" "$ROOT\scripts\" }
    if (-not $WhatIf) { ruff format --check "$ROOT\src\" "$ROOT\tests\" "$ROOT\scripts\" }
}

if ($Scope -eq "all" -or $Scope -eq "typecheck") {
    Write-Step "=== Running mypy type checker ==="
    if (-not $WhatIf) { mypy "$ROOT\src\" --ignore-missing-imports }
}

if ($Scope -eq "all" -or $Scope -eq "unit") {
    Write-Step "=== Running unit tests ==="
    if (-not $WhatIf) { pytest "$ROOT\tests\unit" -m unit --tb=short -x --no-header -q }
}

if ($Scope -eq "all" -or $Scope -eq "integration") {
    Write-Step "=== Running integration tests ==="
    if (-not $WhatIf) { pytest "$ROOT\tests\integration" -m integration --tb=short -x --no-header -q }
}

if ($Scope -eq "all") {
    Write-Step "=== Running full test suite ==="
    if (-not $WhatIf) { pytest "$ROOT\tests\" --tb=short -x --no-header -q --ignore=$ROOT\tests\end-to-end --ignore=$ROOT\tests\performance --ignore=$ROOT\tests\security }
}

Write-Step "Done."
