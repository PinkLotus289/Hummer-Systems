# Referral System API

Простая реферальная система на **Django + Django REST Framework + PostgreSQL**.  
Развёрнута для тестирования на (https://www.pythonanywhere.com/)

## 🚀 Функционал

- Авторизация по номеру телефона с имитацией отправки кода (4 цифры, задержка 1–2 сек).
- Регистрация нового пользователя при первой авторизации.
- Генерация 6‑значного инвайт‑кода (цифры + буквы) при первой авторизации.
- Получение профиля пользователя (номер телефона, свой инвайт‑код, активированный чужой код, список рефералов).
- Ввод чужого инвайт‑кода (проверка на существование, один раз на пользователя).
- Список рефералов в профиле.

## 📡 API

Все запросы работают с `JSON`.  
Авторизация по токену: `Authorization: Bearer <token>`.

---

### ▶️ Авторизация: запрос кода

- Отправляет код подтверждения на указанный номер.

**POST** `/auth/phone/`

- json

Request:
{
  "phone_number": "+79991234567"
}

Response:
{
  "status": "ok",
  "message": "Code sent"
}

### ▶️ Авторизация: проверка кода

- Проверяет код и возвращает токены авторизации.

**POST** `/auth/verify/`

- json

Request:
{
  "phone_number": "+79991234567",
  "code": "1234"
}

Response:
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "phone_number": "+79991234567",
    "invite_code": "QXIMS0",
    "created": true
}

### ▶️ Получение профиля

- Требует авторизацию. Возвращает информацию о пользователе.

**GET** `/auth/profile/`

- json

Response:
{
  "phone_number": "+79991234567",
  "invite_code": "A1B2C3",
  "activated_invite_code": QXIMAA,
  "referrals": 
    "+79995556677",
    "+79991112233"
}

### ▶️ Ввод чужого инвайт‑кода

- Требует авторизацию. Активирует чужой код (если ещё не активирован).

**POST** `/auth/profile/use_invite/`

- json

Request:
{
  "invite_code": "XYZ789"
}

Response (успех):
{
  "message": "Инвайт‑код XYZ789 успешно активирован."
}

Response (если уже активирован):
{
"error": "Нельзя активировать свой собственный инвайт‑код."
}

Response (если код не найден):
{
  "error": "Код не найден."
}

### ReDoc

✅ ReDoc документация:
`/api/docs/redoc/`

✅ Swagger UI:
`/api/docs/swagger/`

✅ OpenAPI JSON:
`/api/schema/`

## Структура базы данных

- User

id,
phone,
invite_code,
activated_invite_code (nullable)

