# MindSchool

Приложение на **FastAPI** + **Telegram Bot** + **PostgreSQL**, полностью запускаемое через Docker Compose.

---

## Требования

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Файл `.env` в корне проекта с переменными окружения:

Нужно получить Токен бота через BotFather и вставить
Нужно в корне проекта создать файл .env
```env
API_URL=...
BOT_TOKEN=<токен твоего бота>

DB_HOST=...
DB_PORT=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
```
Можно скопировать данные из .env.container
Останеться только токен бота вставить


Скачиваем проект с github
Командой ```git clone```

Для запуска выполнить команду
Команды запускаем из корня приложения
```
docker compose up или docker compose up -d (чтобы не выводились логи в консоль)
```

Документация будет доступна по адресу
http://localhost:8000/docs
