@echo off
title ScamShield AI Launcher
cd /d "C:\Users\mr\.gemini\antigravity-ide\scratch\keerthanajain"

echo ========================================================
echo        Starting ScamShield AI Desktop Application
echo ========================================================

:: Check if server is responding
powershell -Command "try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/health' -TimeoutSec 1; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting local background engine...
    start /min "ScamShield Server" "C:\Users\mr\AppData\Local\Programs\Python\Python312\python.exe" app.py
    timeout /t 2 /nobreak >nul
)

:: Launch in native standalone window mode using Edge
echo Launching application window...
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:5000 --window-size=980,820

exit
