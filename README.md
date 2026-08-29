# 💬 FastAPI Messages CRUD API

Простой REST API сервис для управления сообщениями, демонстрирующий реализацию базовых CRUD-операций (Create, Read, Update, Delete) с использованием in-memory хранилища данных.

---

## 🛠 Стек технологий

* **Язык:** Python 3.11+
* **Фреймворк:** FastAPI
* **ASGI-сервер:** Uvicorn
* **Хранилище:** In-Memory Dict (`message_db`)

---

## ⚙️ Функционал API

- [x] **GET `/messages`** — Получение всех сообщений
- [x] **GET `/messages/{message_id}`** — Получение сообщения по его ID (возвращает 404, если не найдено)
- [x] **POST `/messages`** — Создание нового сообщения (с автоинкрементом ID и статусом `201 Created`)
- [x] **PUT `/messages/{message_id}`** — Обновление текста сообщения по ID
- [x] **DELETE `/messages/{message_id}`** — Удаление конкретного сообщения по ID
- [x] **DELETE `/messages`** — Полная очистка базы сообщений

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone [https://github.com/Azonjou/python-crud-app.git](https://github.com/Azonjou/python-crud-app.git)
cd python-crud-app