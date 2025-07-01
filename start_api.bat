@echo off
setlocal

REM Set port number and path to your project
set PORT=8000
set VENV_PATH=C:\Users\Rashad\source\repos\WhatsApp-Selenium\venv\Scripts\activate.bat
set PROJECT_DIR=C:\Users\Rashad\source\repos\WhatsApp-Selenium

REM Check if port is in use and get the PID
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%PORT%" ^| findstr "LISTENING"') do (
    echo Terminating process on port %PORT% with PID %%a...
    taskkill /F /PID %%a > nul 2>&1
)

REM Navigate to project directory and activate environment
cd /d %PROJECT_DIR%
call %VENV_PATH%

REM Start Uvicorn
echo Starting Uvicorn...
uvicorn api:app --host 127.0.0.1 --port %PORT% --reload

endlocal
pause
