@echo off
REM BBQ Restaurant AI - Start Both Servers (Windows)
REM This script opens two terminals and starts the backend and frontend

setlocal enabledelayedexpansion

REM Get the project root directory
set PROJECT_ROOT=%~dp0

echo.
echo ================================================
echo   BBQ Restaurant AI - Starting Servers
echo ================================================
echo.
echo Opening two new terminal windows...
echo.

REM Start Backend in new terminal
echo Starting Backend (FastAPI on port 8000)...
start cmd /k "cd /d "%PROJECT_ROOT%" && python -m uvicorn app.main:app --reload --port 8000"

REM Wait a bit for backend to start
timeout /t 2 /nobreak

REM Start Frontend in new terminal
echo Starting Frontend (React on port 3000)...
start cmd /k "cd /d "%PROJECT_ROOT%frontend" && npm run dev"

REM Wait for frontend to start
timeout /t 3 /nobreak

REM Open browser
echo.
echo ================================================
echo   Opening Dashboard in Browser...
echo ================================================
echo.
start http://localhost:3000

echo.
echo ✓ Both servers are starting!
echo.
echo Frontend Dashboard: http://localhost:3000
echo API Documentation:  http://localhost:8000/docs
echo.
echo The terminal windows will stay open so you can see the logs.
echo Press Ctrl+C in either window to stop that server.
echo.
pause
