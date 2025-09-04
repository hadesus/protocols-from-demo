## Документация по API

### Обзор

API предоставляет эндпоинты для загрузки, анализа и экспорта клинических протоколов.

### Эндпоинты

#### 1. Загрузка и анализ протокола

- **URL**: `/api/upload`
- **Метод**: `POST`
- **Описание**: Загружает DOCX файл, анализирует его и возвращает результат.
- **Тело запроса**: `multipart/form-data` с полем `file`
- **Ответ (успех)**:

```json
{
  "success": true,
  "protocol_summary": "...",
  "main_condition": "...",
  "drugs": [...],
  "analysis_timestamp": "..."
}
```

- **Ответ (ошибка)**:

```json
{
  "error": "..."
}
```

#### 2. Поиск исследований

- **URL**: `/api/research/<drug_name>`
- **Метод**: `GET`
- **Описание**: Ищет исследования для указанного препарата.
- **Параметры URL**: `drug_name` (string, required)
- **Параметры запроса**: `condition` (string, optional)
- **Ответ**:

```json
{
  "pubmed": [...],
  "clinical_trials": [...],
  "fda": [...]
}
```

#### 3. Экспорт в PDF

- **URL**: `/api/export/pdf`
- **Метод**: `POST`
- **Описание**: Экспортирует результаты анализа в PDF файл.
- **Тело запроса**: JSON с данными анализа
- **Ответ**:

```json
{
  "pdf_url": "/api/download/..."
}
```

#### 4. Скачивание файла

- **URL**: `/api/download/<filename>`
- **Метод**: `GET`
- **Описание**: Скачивает сгенерированный файл.
- **Параметры URL**: `filename` (string, required)

#### 5. Проверка состояния

- **URL**: `/api/health`
- **Метод**: `GET`
- **Описание**: Проверяет состояние сервиса.
- **Ответ**:

```json
{
  "status": "healthy",
  "version": "2.0.0",
  "services": {
    "gemini_ai": true,
    "pubmed": true,
    "clinical_trials": true,
    "fda": true
  }
}
```

