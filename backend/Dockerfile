FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ ./src/

# Создаем необходимые директории
RUN mkdir -p src/downloads src/uploads

# Устанавливаем переменные окружения
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 5000

# Команда запуска
CMD ["python", "src/main.py"]

