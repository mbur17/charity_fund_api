# Charity Fund API — Благотворительная платформа на FastAPI

## Описание
API-сервис для управления благотворительными проектами и пожертвованиями.
Проекты наполняются средствами по принципу FIFO: пожертвования сначала идут в более ранние открытые проекты.

## Технологии
- Python 3.9+
- FastAPI
- SQLAlchemy (async)
- Pydantic
- Alembic
- SQLite (по умолчанию)
- Uvicorn (dev-сервер)
- Pytest

## Установка и запуск

1. Клонируй репозиторий:
```bash
git clone https://github.com/your-username/cat_charity_fund.git
cd cat_charity_fund
```

2. Создай и активируй виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

3. Установи зависимости:
```bash
pip install -r requirements.txt
```

4. Создай файл `.env` и задай переменные:
```bash
APP_TITLE=app-title
APP_DESCRIPTION=app-description
DATABASE_URL=sqlite+aiosqlite:///./db-name.db  # По умолчанию sqlite+aiosqlite:///./app.db
SECRET=your-super-secret-key  # JWT-секрет для подписи токенов
# Для подключения Google отчетности добавь переменные для сервисного аккаунта
# Данные сервисного аккаунта (можно взять из JSON-файла ключа)
TYPE=service_account
PROJECT_ID=your-project-id
PRIVATE_KEY_ID=your-private-key-id
# Обрати внимание: PRIVATE_KEY должен быть в одну строку, все \n — экранированы.
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=your-service-account@your-project-id.iam.gserviceaccount.com
CLIENT_ID=123456789012345678901
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com
# Email пользователя, которому будет выдан доступ к таблице
EMAIL=your-email@gmail.com
```

5. Примени миграции
```bash
alembic upgrade head
```

6. Запусти проект:
```bash
uvicorn app.main:app
```

## Тестирование
```bash
pytest
```

## Документация API

- Swagger UI (интерактивная документация): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc (разметка OpenAPI): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Примеры запросов и ответов

### 1. Создание нового проекта (POST `/charity_project/`) — только для суперюзера

**Запрос:**
```http
POST /charity_project/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Поддержка приюта для животных",
  "description": "Сбор средств на корм и лекарства для животных",
  "full_amount": 10000
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Поддержка приюта для животных",
  "description": "Сбор средств на корм и лекарства для животных",
  "full_amount": 10000,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2024-05-01T12:00:00",
  "close_date": null
}
```

---

### 2. Создание пожертвования (POST `/donation/`) — для авторизованного пользователя

**Запрос:**
```http
POST /donation/
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "full_amount": 3000,
  "comment": "На добрые дела"
}
```

**Ответ:**
```json
{
  "id": 1,
  "full_amount": 3000,
  "comment": "На добрые дела",
  "create_date": "2024-05-01T12:05:00"
}
```

---

### 3. Получить список всех проектов (GET `/charity_project/`) — доступно всем

**Запрос:**
```http
GET /charity_project/
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Поддержка приюта для животных",
    "description": "Сбор средств на корм и лекарства для животных",
    "full_amount": 10000,
    "invested_amount": 3000,
    "fully_invested": false,
    "create_date": "2024-05-01T12:00:00",
    "close_date": null
  }
]
```

---

### 4. Получить свои пожертвования (GET `/donation/my`) — только для пользователя

**Запрос:**
```http
GET /donation/my
Authorization: Bearer <user_token>
```

**Ответ:**
```json
[
  {
    "id": 1,
    "full_amount": 3000,
    "comment": "На добрые дела",
    "create_date": "2024-05-01T12:05:00"
  }
]
```

---

### 5. Удаление проекта (DELETE `/charity_project/{id}`) — только для суперюзера

**Запрос:**
```http
DELETE /charity_project/1
Authorization: Bearer <admin_token>
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Поддержка приюта для животных",
  "description": "Сбор средств на корм и лекарства для животных",
  "full_amount": 10000,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2024-05-01T12:00:00",
  "close_date": null
}
```

### 6. Генерация отчёта по закрытым проектам (POST `/charity_project/google/`) — только для суперюзера
Эндпоинт генерирует Google-таблицу с отчётом по закрытым благотворительным проектам, отсортированным по скорости сбора средств (от самых быстрых).
В таблице отображаются:
- название проекта
- продолжительность сбора
- описание

**Запрос:**
```http
POST /charity_project/google/
Authorization: Bearer <admin_token>
```

**Ответ:**
```json
{
  "projects": [
    {
      "name": "Кошка Мурка",
      "duration": 2.01,
      "description": "Сбор на стерилизацию и вакцинацию"
    },
    {
      "name": "Кот Барсик",
      "duration": 4.52,
      "description": "Помощь при травме лапы"
    }
  ],
  "spreadsheet_url": "https://docs.google.com/spreadsheets/d/1AbCDeFGHIjkLMNOPQRstuVWXYZ"
}
```

## Автор

[Буряковский Максим](https://github.com/yourusername)

## Лицензия

Этот проект распространяется под лицензией MIT.
