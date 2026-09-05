@echo off
REM ============================================================
REM BBQ Dashboard - Diagnostic Script
REM Checks if everything is set up correctly
REM ============================================================

echo.
echo ========================================
echo BBQ Dashboard - Diagnostic Check
echo ========================================
echo.

REM Check Node.js
echo [1/5] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✓ Node.js found: %NODE_VERSION%
) else (
    echo ✗ Node.js NOT FOUND
    echo   Download from: https://nodejs.org
    pause
    exit /b 1
)

REM Check npm
echo [2/5] Checking npm...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
    echo ✓ npm found: %NPM_VERSION%
) else (
    echo ✗ npm NOT FOUND
    pause
    exit /b 1
)

REM Check Python
echo [3/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✓ Python found: %PYTHON_VERSION%
) else (
    echo ✗ Python NOT FOUND
    echo   Download from: https://python.org
    pause
    exit /b 1
)

REM Check if in correct directory
echo [4/5] Checking directories...
if exist "src\components\Dashboard.jsx" (
    echo ✓ Frontend directory found
) else (
    echo ✗ Frontend directory NOT found
    echo   Run this script from frontend folder
    pause
    exit /b 1
)

if exist "..\backend\main.py" (
    echo ✓ Backend directory found
) else (
    echo ⚠ Backend directory may not be accessible
)

REM Check node_modules
echo [5/5] Checking dependencies...
if exist "node_modules" (
    echo ✓ Dependencies installed (node_modules exists)
) else (
    echo ⚠ Dependencies NOT installed
    echo   Run: npm install
)

echo.
echo ========================================
echo All Checks Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Start Backend (in separate terminal):
echo    cd ..\backend
echo    python main.py
echo.
echo 2. Start Frontend (in this terminal):
echo    npm run dev
echo.
echo 3. Open Browser:
echo    http://localhost:3000
echo.
pause
