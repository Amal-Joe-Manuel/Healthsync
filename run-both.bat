@echo off
REM Run backend and frontend at the same time (opens two terminal windows)
REM Backend folder: edit NEXT line if your backend is not in ..\backend
set BACKEND_DIR=%~dp0..\backend
set FRONTEND_DIR=%~dp0

start "HealthSync Backend (port 8000)" cmd /k "cd /d "%BACKEND_DIR%" && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul
start "HealthSync Frontend (port 8080)" cmd /k "cd /d "%FRONTEND_DIR%" && python -m http.server 8080"

echo.
echo Both servers starting in new windows.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:8080  <- open this in your browser
echo.
pause
