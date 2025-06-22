@echo off
REM Check if port 8000 is already in use
netstat -ano | findstr ":8000" > nul
if %ERRORLEVEL% == 0 (
    echo Port 8000 is already in use. Assuming Uvicorn is running.
) else (
    echo Port 8000 is free. Starting Uvicorn...
    cd C:\Users\Rashad\source\repos\WhatsApp-Selenium
    call C:\Users\Rashad\source\repos\WhatsApp-Selenium\venv\Scripts\activate.bat
    uvicorn api:app --host 127.0.0.1 --port 8000 --reload
)
pause