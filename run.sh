#!/bin/sh

echo "Installing uv..."
pip install uv

# Проверяем наличие frontend
if [ ! -d "frontend" ]; then
  echo "Error: folder frontend was not found!"
  exit 1
fi

frontend_port=8080

# Проверяем порт фронтенда
check_port() {
  while nc -z localhost "$frontend_port"; do
    frontend_port=$((frontend_port + 1))
  done
}

check_port

# Запускаем серверы
echo "Starting the server..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:$frontend_port"

# Запуск backend в новом терминале (зависит от системы)
cd backend && nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Запуск frontend в новом терминале (зависит от системы)
# !!! Перед запуском выполнить сборку (npm run build в ./frontend)
cd frontend && nohup npx http-server dist --port $frontend_port

echo "Servers started in background. Check backend.log and frontend.log for output."
echo "Press any key to exit..."
read -n 1 -s