FROM python:3.10-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код (main.py и папку static)
COPY . .

# Открываем порт 8000 для FastAPI
EXPOSE 8000

# Запускаем сервер
CMD ["python", "main.py"]
