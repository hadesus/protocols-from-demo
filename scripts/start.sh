#!/bin/bash

# Скрипт для быстрого запуска анализатора клинических протоколов

set -e

echo "🚀 Запуск анализатора клинических протоколов..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose и попробуйте снова."
    exit 1
fi

# Проверяем наличие файла .env
if [ ! -f .env ]; then
    echo "📝 Создаем файл .env из шаблона..."
    cp .env.docker .env
    echo "⚠️  ВАЖНО: Отредактируйте файл .env и добавьте ваш GEMINI_API_KEY"
    echo "   Затем запустите скрипт снова."
    exit 1
fi

# Проверяем наличие API ключа
if grep -q "your_gemini_api_key_here" .env; then
    echo "⚠️  ВНИМАНИЕ: Пожалуйста, добавьте ваш GEMINI_API_KEY в файл .env"
    echo "   Откройте файл .env и замените 'your_gemini_api_key_here' на ваш реальный API ключ"
    exit 1
fi

echo "🔧 Собираем и запускаем контейнеры..."

# Останавливаем существующие контейнеры
docker-compose down 2>/dev/null || true

# Собираем и запускаем
docker-compose up --build -d

echo "⏳ Ждем запуска сервисов..."
sleep 10

# Проверяем статус сервисов
echo "🔍 Проверяем статус сервисов..."

if curl -f http://localhost:5000/api/health &>/dev/null; then
    echo "✅ Backend запущен успешно"
else
    echo "❌ Backend не отвечает"
    docker-compose logs backend
    exit 1
fi

if curl -f http://localhost:80 &>/dev/null; then
    echo "✅ Frontend запущен успешно"
else
    echo "❌ Frontend не отвечает"
    docker-compose logs frontend
    exit 1
fi

echo ""
echo "🎉 Анализатор клинических протоколов успешно запущен!"
echo ""
echo "📱 Откройте в браузере: http://localhost"
echo "🔧 API доступен по адресу: http://localhost:5000"
echo ""
echo "📋 Полезные команды:"
echo "   Остановить:     docker-compose down"
echo "   Перезапустить:  docker-compose restart"
echo "   Логи:          docker-compose logs -f"
echo "   Статус:        docker-compose ps"
echo ""

