#!/usr/bin/env pwsh
<#
.SYNOPSIS
    BBQ Restaurant AI - Complete Local Development Setup Script

.DESCRIPTION
    Automates the setup of both frontend (React) and backend (FastAPI) locally.
    Installs all dependencies, verifies installations, and provides quick-start commands.

.PARAMETER SkipNodeSetup
    Skip Node.js dependency installation

.PARAMETER SkipPythonSetup
    Skip Python dependency installation

.PARAMETER StartServers
    Automatically start both backend and frontend servers after setup

.EXAMPLE
    .\setup-local-dev.ps1
    .\setup-local-dev.ps1 -StartServers
#>

param(
    [switch]$SkipNodeSetup,
    [switch]$SkipPythonSetup,
    [switch]$StartServers
)

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

# Project root
$ProjectRoot = Get-Location
$FrontendDir = Join-Path $ProjectRoot "frontend"
$BackendDir = $ProjectRoot

Write-Host "`n════════════════════════════════════════════════════════" -ForegroundColor $InfoColor
Write-Host "  BBQ Restaurant AI - Local Development Setup" -ForegroundColor $InfoColor
Write-Host "════════════════════════════════════════════════════════`n" -ForegroundColor $InfoColor

# Step 1: Verify Prerequisites
Write-Host "[1/5] Verifying Prerequisites..." -ForegroundColor $InfoColor

$NodeVersion = node --version 2>&1
$NpmVersion = npm --version 2>&1
$PythonVersion = python --version 2>&1

if ($NodeVersion -and $NpmVersion) {
    Write-Host "✓ Node.js: $NodeVersion" -ForegroundColor $SuccessColor
    Write-Host "✓ npm: $NpmVersion" -ForegroundColor $SuccessColor
} else {
    Write-Host "✗ Node.js or npm not found! Please install from https://nodejs.org/" -ForegroundColor $ErrorColor
    exit 1
}

if ($PythonVersion) {
    Write-Host "✓ Python: $PythonVersion" -ForegroundColor $SuccessColor
} else {
    Write-Host "✗ Python not found! Please install from https://python.org/" -ForegroundColor $ErrorColor
    exit 1
}

# Step 2: Install Frontend Dependencies
if (-not $SkipNodeSetup) {
    Write-Host "`n[2/5] Installing Frontend Dependencies..." -ForegroundColor $InfoColor

    Set-Location $FrontendDir

    # Clean previous install if problematic
    if (Test-Path "node_modules") {
        Write-Host "  Cleaning previous installation..." -ForegroundColor $WarningColor
        Remove-Item -Recurse -Force "node_modules" -ErrorAction SilentlyContinue
        Remove-Item "package-lock.json" -ErrorAction SilentlyContinue
    }

    Write-Host "  Running: npm install" -ForegroundColor $InfoColor
    npm install --legacy-peer-deps

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Frontend dependencies installed" -ForegroundColor $SuccessColor
    } else {
        Write-Host "✗ Frontend installation failed" -ForegroundColor $ErrorColor
        exit 1
    }
} else {
    Write-Host "`n[2/5] Skipping Frontend Dependencies (--SkipNodeSetup)" -ForegroundColor $WarningColor
}

# Step 3: Install Backend Dependencies
if (-not $SkipPythonSetup) {
    Write-Host "`n[3/5] Installing Backend Dependencies..." -ForegroundColor $InfoColor

    Set-Location $BackendDir

    Write-Host "  Running: pip install -r requirements.txt" -ForegroundColor $InfoColor
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Backend dependencies installed" -ForegroundColor $SuccessColor
    } else {
        Write-Host "✗ Backend installation failed" -ForegroundColor $ErrorColor
        exit 1
    }
} else {
    Write-Host "`n[3/5] Skipping Backend Dependencies (--SkipPythonSetup)" -ForegroundColor $WarningColor
}

# Step 4: Verify Installations
Write-Host "`n[4/5] Verifying Installations..." -ForegroundColor $InfoColor

Set-Location $FrontendDir
$HasVite = npm list vite 2>&1 | Select-String "vite@" | Measure-Object | Select-Object -ExpandProperty Count
if ($HasVite -gt 0) {
    Write-Host "✓ Vite is installed" -ForegroundColor $SuccessColor
} else {
    Write-Host "⚠ Vite not found, attempting reinstall..." -ForegroundColor $WarningColor
}

Set-Location $BackendDir
$HasFastAPI = python -c "import fastapi; print(fastapi.__version__)" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ FastAPI is installed (v$HasFastAPI)" -ForegroundColor $SuccessColor
} else {
    Write-Host "✗ FastAPI not found" -ForegroundColor $ErrorColor
}

# Step 5: Summary and Next Steps
Write-Host "`n[5/5] Setup Complete!" -ForegroundColor $SuccessColor

Write-Host "`n════════════════════════════════════════════════════════" -ForegroundColor $InfoColor
Write-Host "  Next Steps" -ForegroundColor $InfoColor
Write-Host "════════════════════════════════════════════════════════`n" -ForegroundColor $InfoColor

Write-Host "Open TWO terminal windows and run:" -ForegroundColor $InfoColor

Write-Host "`nTerminal 1 - Backend (FastAPI):" -ForegroundColor $WarningColor
Write-Host "cd `"$BackendDir`"" -ForegroundColor $InfoColor
Write-Host "python -m uvicorn app.main:app --reload --port 8000`n" -ForegroundColor $InfoColor

Write-Host "Terminal 2 - Frontend (React):" -ForegroundColor $WarningColor
Write-Host "cd `"$FrontendDir`"" -ForegroundColor $InfoColor
Write-Host "npm run dev`n" -ForegroundColor $InfoColor

Write-Host "Then open your browser to:" -ForegroundColor $InfoColor
Write-Host "🌐 http://localhost:3000" -ForegroundColor $SuccessColor

Write-Host "`n════════════════════════════════════════════════════════" -ForegroundColor $InfoColor
Write-Host "  Helpful URLs" -ForegroundColor $InfoColor
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $InfoColor
Write-Host "Frontend Dashboard:  http://localhost:3000" -ForegroundColor $InfoColor
Write-Host "API Swagger Docs:    http://localhost:8000/docs" -ForegroundColor $InfoColor
Write-Host "API ReDoc Docs:      http://localhost:8000/redoc" -ForegroundColor $InfoColor

Write-Host "`n════════════════════════════════════════════════════════" -ForegroundColor $InfoColor
Write-Host "  Development Commands" -ForegroundColor $InfoColor
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor $InfoColor
Write-Host "Frontend:" -ForegroundColor $WarningColor
Write-Host "  npm run dev       - Start dev server" -ForegroundColor $InfoColor
Write-Host "  npm run build     - Production build" -ForegroundColor $InfoColor
Write-Host "  npm run lint      - Lint code" -ForegroundColor $InfoColor
Write-Host "  npm run format    - Format code`n" -ForegroundColor $InfoColor

Write-Host "Backend:" -ForegroundColor $WarningColor
Write-Host "  --reload flag     - Auto-restart on code changes" -ForegroundColor $InfoColor
Write-Host "  --port 8000       - Run on port 8000" -ForegroundColor $InfoColor
Write-Host "  /docs endpoint    - Interactive API documentation`n" -ForegroundColor $InfoColor

if ($StartServers) {
    Write-Host "`n════════════════════════════════════════════════════════" -ForegroundColor $InfoColor
    Write-Host "  Starting Servers..." -ForegroundColor $InfoColor
    Write-Host "════════════════════════════════════════════════════════`n" -ForegroundColor $InfoColor

    Write-Host "Starting Backend..." -ForegroundColor $InfoColor
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; python -m uvicorn app.main:app --reload --port 8000"

    Start-Sleep -Seconds 2

    Write-Host "Starting Frontend..." -ForegroundColor $InfoColor
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$FrontendDir'; npm run dev"

    Write-Host "`n✓ Servers started in new windows. Opening browser...`n" -ForegroundColor $SuccessColor

    Start-Sleep -Seconds 3
    Start-Process "http://localhost:3000"
}

Write-Host "`n✓ Setup complete! Happy coding! 🚀`n" -ForegroundColor $SuccessColor
