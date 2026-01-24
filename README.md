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


# DRF-проект на виртуальной машине Yandex Cloud через CI/CD

Backend-часть веб-приложения, реализованная с использованием Django REST Framework.
Проект развёрнут на удалённом сервере через виртуальную машину на Yandex Cloud.

## Развёртывание на сервере (ручной деплой)

Проект развёрнут на удалённом сервере под управлением виртуальной машины на Ubuntu.

### 1. Подготовка сервера

На сервере установлены необходимые пакеты:

```
sudo apt update
sudo apt upgrade
```

Настройка Docker (по инструкции на официальном сайте):
```
https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

```

### 2. Настройка Firewall и порты 80, 443, 22

Откройте порты для http, https и ssh:
```
sudo ufw status
```
```
sudo ufw enable
```
```
sudo ufw allow 80/tcp
```
```
sudo ufw allow 443/tcp
```
```
sudo ufw allow 22/tcp
```
После открытия портов проверьте настройки, чтобы убедиться, что правила применились:
```
sudo ufw status
```

### 3. Зависимости

Установка зависимостей:

```pip install flake8```

```pip freeze > requirements.txt```

### 4. Переменные окружения

В корне проекта используется файл .env (не добавляется в репозиторий). Пример шаблона находится в .env.sample.

### - Nginx (при необходимости)

Nginx используется как reverse proxy для проксирования запросов к Gunicorn.

Настройте конфигурацию в файле nginx.conf: глобальные директивы, которые определяют общие настройки для всего сервера.

Приложение доступно по публичному IP-адресу сервера.

### - Docker

В проекте подготовьте:
`Dockerfile`
`.dockerignore`
`docker-compose.yaml`

Docker используется как подготовка к автоматическому деплою.

### Безопасность (минимальная настройка)

- Подключение к серверу выполняется по SSH.

### CI/CD (GitHub Actions)

Workflow расположен в репозитории: `.github/workflows/ci.yml`

При каждом `push` в ветку выполняется:

- установка зависимостей

- запуск тестов и миграций

- деплой на сервер по SSH (только если тесты прошли)

Для работы деплоя используются GitHub Secrets:

- DB_HOST - хост БД
- DB_NAME - наименование БД
- DB_PASSWORD - пароль к БД
- DB_USER - имя пользователя БД
- DOCKER_HUB_ACCESS_TOKEN - токен доступа на DockerHUB
- DOCKER_HUB_USERNAME - логин пользователя на DockerHUB
- SECRET_KEY - Django-SECRET_KEY
- SERVER_IP - адрес сервера на ВМ
- SSH_KEY - SSH-ключ безопасности
- SSH_USER - логин пользователя SSH-ключа
