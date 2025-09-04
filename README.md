# Clinical Protocol Analyzer

Современный анализатор клинических протоколов с модульной архитектурой, интеграцией с медицинскими базами данных и расширенными возможностями анализа.

## Особенности

- 🔬 **Анализ протоколов**: Автоматический анализ DOCX файлов клинических протоколов
- 🔍 **Поиск исследований**: Интеграция с PubMed, ClinicalTrials.gov, openFDA
- 🤖 **ИИ анализ**: Использование Gemini AI для извлечения и анализа данных
- 📊 **Отчеты**: Генерация детальных отчетов в различных форматах
- 🏗️ **Модульная архитектура**: Разделение на frontend и backend
- 🔒 **Безопасность**: Защищенное хранение API ключей
- 📱 **Адаптивный дизайн**: Поддержка мобильных устройств

## Архитектура

```
clinical-protocol-analyzer/
├── frontend/          # React.js приложение
├── backend/           # Flask API сервер
├── docs/             # Документация
├── examples/         # Примеры использования
└── docker/           # Docker конфигурация
```

## Быстрый старт

### Требования

- Node.js 18+
- Python 3.8+
- Git

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/clinical-protocol-analyzer.git
cd clinical-protocol-analyzer
```

2. Настройте backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Настройте frontend:
```bash
cd ../frontend
pnpm install
```

4. Настройте переменные окружения:
```bash
cp backend/.env.example backend/.env
# Отредактируйте .env файл с вашими API ключами
```

### Запуск

1. Запустите backend:
```bash
cd backend
source venv/bin/activate
python src/main.py
```

2. Запустите frontend:
```bash
cd frontend
pnpm run dev
```

3. Откройте http://localhost:5173 в браузере

## API Ключи

Для работы приложения необходимы следующие API ключи:

- **Gemini AI**: Для анализа текста протоколов
- **PubMed**: Для поиска научных публикаций (опционально)
- **ClinicalTrials.gov**: Для поиска клинических исследований (опционально)
- **openFDA**: Для получения регуляторной информации (опционально)

## Разработка

### Структура проекта

- `frontend/src/components/` - React компоненты
- `frontend/src/services/` - API сервисы
- `backend/src/routes/` - Flask маршруты
- `backend/src/services/` - Бизнес-логика
- `backend/src/models/` - Модели данных

### Добавление новых функций

1. Создайте новый компонент в `frontend/src/components/`
2. Добавьте API эндпоинт в `backend/src/routes/`
3. Реализуйте бизнес-логику в `backend/src/services/`
4. Обновите документацию

## Развертывание

### Docker

```bash
docker-compose up -d
```

### Ручное развертывание

1. Соберите frontend:
```bash
cd frontend
pnpm run build
```

2. Скопируйте собранные файлы в backend/src/static/
3. Запустите Flask приложение в production режиме

## Лицензия

MIT License - см. [LICENSE](LICENSE) файл для деталей.

## Вклад в проект

1. Форкните репозиторий
2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## Поддержка

Если у вас есть вопросы или проблемы, создайте [issue](https://github.com/your-username/clinical-protocol-analyzer/issues) в репозитории.

