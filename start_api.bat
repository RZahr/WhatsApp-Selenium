@echo off
cd C:\Users\Rashad\source\repos\WhatsApp-Selenium
call C:\Users\Rashad\source\repos\WhatsApp-Selenium\venv\Scripts\activate.bat
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
pause