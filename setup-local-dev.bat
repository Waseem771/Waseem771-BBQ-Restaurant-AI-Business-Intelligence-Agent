@echo off
REM BBQ Restaurant AI - Quick Start Setup (Windows Batch)
REM This script sets up and runs the entire project locally

setlocal enabledelayedexpansion

cls
echo ================================================
echo   BBQ Restaurant AI - Local Setup
echo ================================================
echo.

REM Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install from https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo OK: Node.js %NODE_VER%

REM Check npm
echo Checking npm installation...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm not found.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set NPM_VER=%%i
echo OK: npm %NPM_VER%

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install from https://python.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PY_VER=%%i
echo OK: %PY_VER%

echo.
echo ================================================
echo   Installing Frontend Dependencies...
echo ================================================
echo.

cd frontend
if exist "node_modules" (
    echo Cleaning previous installation...
    rmdir /s /q node_modules >nul 2>&1
    del package-lock.json >nul 2>&1
)

echo Running: npm install
npm install --legacy-peer-deps
if errorlevel 1 (
    echo ERROR: Frontend installation failed
    pause
    exit /b 1
)

cd ..
echo.
echo ================================================
echo   Installing Backend Dependencies...
echo ================================================
echo.

echo Running: pip install -r requirements.txt
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Backend installation failed
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To start your development environment:
echo.
echo [Terminal 1 - Backend]
echo cd "%cd%"
echo python -m uvicorn app.main:app --reload --port 8000
echo.
echo [Terminal 2 - Frontend]
echo cd "%cd%\frontend"
echo npm run dev
echo.
echo Then open your browser to:
echo http://localhost:3000
echo.
echo Helpful URLs:
echo - Dashboard:       http://localhost:3000
echo - API Docs:        http://localhost:8000/docs
echo - API ReDoc:       http://localhost:8000/redoc
echo.
pause
