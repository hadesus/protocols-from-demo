# Руководство по Docker

## Обзор

Проект поддерживает запуск через Docker для упрощения развертывания и обеспечения консистентности среды выполнения.

## Архитектура Docker

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (React +      │◄──►│   (Flask API)   │
│    Nginx)       │    │                 │
│   Port: 80      │    │   Port: 5000    │
└─────────────────┘    └─────────────────┘
```

## Компоненты

### Frontend Container
- **Базовый образ**: `node:20-alpine` (сборка) + `nginx:alpine` (production)
- **Порт**: 80
- **Функции**:
  - Сборка React приложения
  - Обслуживание статических файлов через Nginx
  - Проксирование API запросов к backend

### Backend Container
- **Базовый образ**: `python:3.11-slim`
- **Порт**: 5000
- **Функции**:
  - Flask API сервер
  - Анализ протоколов с помощью Gemini AI
  - Интеграция с медицинскими базами данных

## Файлы конфигурации

### docker-compose.yml
Основной файл для production развертывания:
- Автоматическая сборка образов
- Настройка сети между контейнерами
- Монтирование volumes для данных
- Health checks для мониторинга

### docker/docker-compose.dev.yml
Файл для разработки:
- Hot reload для frontend и backend
- Монтирование исходного кода
- Debug режим

### .env.docker
Шаблон переменных окружения:
- API ключи
- Настройки Flask
- Конфигурация CORS

## Команды

### Быстрый запуск
```bash
# Автоматический запуск
./scripts/start.sh

# Остановка
./scripts/stop.sh
```

### Ручное управление
```bash
# Сборка и запуск
docker-compose up --build -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f [service_name]

# Перезапуск сервиса
docker-compose restart [service_name]

# Выполнение команд в контейнере
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Разработка
```bash
# Запуск в режиме разработки
docker-compose -f docker/docker-compose.dev.yml up --build

# Остановка dev среды
docker-compose -f docker/docker-compose.dev.yml down
```

## Volumes

### Постоянные данные
- `./backend/uploads` - загруженные файлы
- `./backend/downloads` - сгенерированные отчеты

### Разработка
- `./backend/src` - исходный код backend (hot reload)
- `./frontend/src` - исходный код frontend (hot reload)

## Сеть

Контейнеры общаются через внутреннюю Docker сеть:
- Frontend → Backend: `http://backend:5000`
- Внешний доступ: `http://localhost:80`

## Мониторинг

### Health Checks
Автоматические проверки состояния:
- Backend: `GET /api/health`
- Frontend: `GET /`

### Логи
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f frontend

# Последние N строк
docker-compose logs --tail=50 backend
```

## Troubleshooting

### Проблемы с портами
```bash
# Проверка занятых портов
netstat -tulpn | grep :80
netstat -tulpn | grep :5000

# Изменение портов в docker-compose.yml
ports:
  - "8080:80"  # вместо 80:80
```

### Проблемы с API ключами
```bash
# Проверка переменных окружения
docker-compose exec backend env | grep GEMINI

# Пересоздание контейнера с новыми переменными
docker-compose up --force-recreate backend
```

### Проблемы с сетью
```bash
# Проверка сети Docker
docker network ls
docker network inspect protocols-from-demo_default

# Пересоздание сети
docker-compose down
docker-compose up
```

### Очистка
```bash
# Удаление контейнеров и образов
docker-compose down --rmi all

# Полная очистка Docker
docker system prune -a

# Удаление volumes
docker-compose down -v
```

## Производительность

### Оптимизация образов
- Многоэтапная сборка для frontend
- Минимальные базовые образы (alpine)
- Кэширование слоев Docker

### Ресурсы
```yaml
# Ограничение ресурсов в docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

## Безопасность

### Переменные окружения
- Никогда не коммитьте .env файлы
- Используйте Docker secrets в production
- Ограничьте доступ к API ключам

### Сеть
- Контейнеры изолированы в собственной сети
- Только необходимые порты открыты наружу
- Nginx как reverse proxy для дополнительной безопасности

## Production Deployment

### Рекомендации
1. Используйте внешнюю базу данных (PostgreSQL)
2. Настройте SSL/TLS сертификаты
3. Используйте Docker Swarm или Kubernetes
4. Настройте мониторинг и логирование
5. Регулярно обновляйте образы

### Пример production конфигурации
```yaml
version: '3.8'
services:
  backend:
    image: your-registry/protocol-analyzer-backend:latest
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://...
    secrets:
      - gemini_api_key
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
```

