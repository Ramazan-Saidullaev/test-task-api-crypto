# Crypto Price API

## Описание проекта

Это API для получения индексных цен криптовалют с Deribit. Проект построен на FastAPI, использует PostgreSQL для хранения данных, Redis для Celery, и Celery для периодического сбора данных.

## Структура проекта

```
test-task-api-crypto/
├── app/
│   ├── main.py                 # Точка входа FastAPI приложения
│   ├── api/
│   │   ├── dependencies.py     # Зависимости для DI
│   │   └── routes/
│   │       └── prices.py       # Роуты для API цен
│   ├── clients/
│   │   └── deribit.py          # Клиент для Deribit API
│   ├── core/
│   │   ├── config.py           # Конфигурация приложения
│   │   └── celery_app.py       # Настройка Celery
│   ├── db/
│   │   └── session.py          # Настройка базы данных
│   ├── models/
│   │   └── price.py            # Модель PriceRecord
│   ├── repositories/
│   │   └── price_repository.py # Репозиторий для работы с ценами
│   ├── schemas/
│   │   ├── common.py           # Общие схемы (Ticker enum)
│   │   └── price.py            # Схемы для цен
│   ├── services/
│   │   └── price_service.py    # Сервис для бизнес-логики цен
│   └── tasks/
│       └── price_tasks.py      # Celery задачи для сбора цен
├── tests/                      # Тесты
├── Dockerfile                  # Docker образ
├── docker-compose.yml          # Docker Compose конфигурация
├── requirements.txt            # Python зависимости
├── pytest.ini                  # Настройки pytest
└── README.md                   # Этот файл
```

## Архитектура

Проект использует чистую архитектуру с разделением на слои:

- **API Layer**: FastAPI роуты для обработки HTTP запросов
- **Service Layer**: Бизнес-логика (PriceService)
- **Repository Layer**: Доступ к данным (PriceRepository)
- **Domain Layer**: Модели данных (PriceRecord)
- **Infrastructure Layer**: Внешние сервисы (DeribitClient, БД, Celery)

## API Описание

### Endpoints

#### GET /prices
Получить все цены для указанного тикера.

**Параметры:**
- `ticker` (query, required): Тикер (btc_usd или eth_usd)

**Пример запроса:**
```
GET /prices?ticker=btc_usd
```

**Пример ответа:**
```json
[
  {
    "id": 1,
    "ticker": "btc_usd",
    "price": "45000.12345678",
    "timestamp_unix": 1640995200
  }
]
```

#### GET /prices/latest
Получить последнюю цену для указанного тикера.

**Параметры:**
- `ticker` (query, required): Тикер (btc_usd или eth_usd)

**Пример запроса:**
```
GET /prices/latest?ticker=btc_usd
```

**Пример ответа:**
```json
{
  "ticker": "btc_usd",
  "price": "45000.12345678",
  "timestamp_unix": 1640995200
}
```

#### GET /prices/by-date
Получить цены для указанного тикера и даты.

**Параметры:**
- `ticker` (query, required): Тикер (btc_usd или eth_usd)
- `date` (query, required): Дата в формате YYYY-MM-DD

**Пример запроса:**
```
GET /prices/by-date?ticker=btc_usd&date=2023-01-01
```

**Пример ответа:**
```json
[
  {
    "id": 1,
    "ticker": "btc_usd",
    "price": "45000.12345678",
    "timestamp_unix": 1640995200
  }
]
```

## Запуск проекта

### Предварительные требования

- Docker и Docker Compose
- Git

### Шаги запуска

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Ramazan-Saidullaev/test-task-api-crypto.git
   cd test-task-api-crypto
   ```

2. **Создайте файл .env (опционально):**
   Если нужно переопределить настройки, создайте файл `.env` в корне проекта:
   ```env
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DATABASE_URL=postgresql+psycopg://crypto_user:crypto_password@db:5432/crypto_prices
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/1
   DERIBIT_BASE_URL=https://www.deribit.com/api/v2
   TRACKED_TICKERS=btc_usd,eth_usd
   ```

3. **Запустите сервисы с помощью Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   Это запустит:
   - API сервер на http://localhost:8000
   - PostgreSQL базу данных на порту 5432
   - Redis на порту 6379
   - Celery worker для сбора данных
   - Celery beat для планирования задач

4. **Проверьте работу API:**
   Откройте в браузере: http://localhost:8000

   Или используйте curl:
   ```bash
   curl "http://localhost:8000/prices/latest?ticker=btc_usd"
   ```

### Остановка

```bash
docker-compose down
```

### Запуск тестов

```bash
docker-compose exec api pytest
```

Или локально (если Python установлен):

```bash
pip install -r requirements.txt
pytest
```

## Разработка

### Локальный запуск без Docker

1. Установите Python 3.12+
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройте переменные окружения в `.env`
4. Запустите PostgreSQL и Redis локально или используйте Docker для них
5. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Запустите Celery worker:
   ```bash
   celery -A app.core.celery_app.celery_app worker --loglevel=info
   ```
7. Запустите Celery beat:
   ```bash
   celery -A app.core.celery_app.celery_app beat --loglevel=info
   ```

## Используемые технологии

- **FastAPI**: Веб-фреймворк для API
- **SQLAlchemy**: ORM для работы с базой данных
- **PostgreSQL**: База данных
- **Celery**: Асинхронные задачи
- **Redis**: Брокер сообщений и кэш
- **Pydantic**: Валидация данных
- **AioHTTP**: Асинхронные HTTP запросы
- **Docker**: Контейнеризация</content>
<parameter name="filePath">