# MindSchool

Приложение на **FastAPI** + **Telegram Bot** + **PostgreSQL**, полностью запускаемое через Docker Compose.

---

## Требования

- [Docker](https://www.docker.com/) 20+
- [Docker Compose](https://docs.docker.com/compose/) 1.29+
- Файл `.env` в корне проекта с переменными окружения:

```env
API_URL=http://api:8000
BOT_TOKEN=<токен твоего бота>

DB_HOST=...
DB_PORT=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
```

Скачиваем проект с github
Для запуска выполнить несколько команд
Запускаем команды из корня приложения
```
docker compose up или docker compose up -d (чтобы не выводились логи в консоль)
```
После того как создадуться образы и контейнеры
нужно будет применить миграции
```
docker exec <container id> alembic upgrade head
```

Документация будет доступна по адресу
http://localhost:8000/docs
