# Запуск приложения через Docker Compose

---

1. Создайте файл `.env` в корне проекта по примеру `.env.example`.
---

2. Запустите проект:

```bash
    docker compose up --build
```
- Запуск в фоновом режиме:
```bash
    docker compose up --build -d
```

---


## Проверка сервисов:

- Backend: http://localhost:8000/

---

- PostgreSQL:
```bash
    docker compose exec db pg_isready -U $POSTGRES_USER -d $POSTGRES_DB
```

---

-  Redis:
```bash
    docker compose exec redis redis-cli ping
```
Ожидаемый ответ: `PONG.`

---

- Celery worker:
```bash
    docker compose logs -f celery
```

---

- Celery beat:
```bash
    docker compose logs -f celery_beat
```