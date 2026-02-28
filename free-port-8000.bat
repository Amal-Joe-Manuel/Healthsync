@echo off
setlocal enabledelayedexpansion
REM Free port 8000 (kills the process using it)
echo Finding process using port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
  echo Killing process ID: %%a
  taskkill /PID %%a /F 2>nul
  if !errorlevel! equ 0 echo Port 8000 freed.
)
echo.
echo If port was in use, you can run run-both.bat again.
echo If you see "Access denied", close the other backend terminal or run this as Administrator.
pause
