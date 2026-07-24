$ErrorActionPreference = "Stop"

$workspaceRoot = "D:\Hack2Skill\Berunda"
$appsailTarget = "$workspaceRoot\appsail\berunda_api"

Write-Host "Building AppSail artifact for Berunda API..."

# Clean old build
if (Test-Path $appsailTarget) {
    Remove-Item -Recurse -Force $appsailTarget
}
New-Item -ItemType Directory -Force -Path $appsailTarget | Out-Null

# Copy source code
Write-Host "Copying src directory..."
Copy-Item -Path "$workspaceRoot\src" -Destination $appsailTarget -Recurse

# Copy requirements
Write-Host "Copying requirements.txt..."
Copy-Item -Path "$workspaceRoot\requirements.txt" -Destination $appsailTarget

# Copy AppSail configuration
Write-Host "Copying app-config.json..."
Copy-Item -Path "$workspaceRoot\appsail_template\app-config.json" -Destination $appsailTarget

Write-Host "AppSail artifact built successfully at $appsailTarget"
Write-Host "You can now run 'catalyst deploy' to push to production."
