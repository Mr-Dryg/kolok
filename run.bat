@echo off

echo Installing uv...
pip install uv

:: Проверяем наличие папки frontend
if not exist "frontend\" (
  echo Error: folder frontend was not found!
  exit /b 1
)

set frontend_port=8080

:: Функция проверки свободного порта
:check_port
netstat -ano | findstr ":%frontend_port%" >nul
if %errorlevel% equ 0 (
  set /a frontend_port+=1
  goto check_port
)

echo Starting the server...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:%frontend_port%

:: Запуск backend в новом окне
start "Backend" cmd /k "cd backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Запуск frontend в новом окне
:: !!! Перед запуском выполнить сборку (npm run build в ./frontend)
start "Frontend" cmd /k "cd frontend && npx http-server dist --port %frontend_port%"


echo Servers started in separate windows
echo Press any key to exit...
pause >nul