#!/bin/bash

# определение .env файла
export ENV_FILE=./.env
MARKETPLACE=marketplace

# Остановка и удаление контейнеров
docker-compose down

# Запуск новых контейнеров 
docker-compose up -d --build

# Запуск миграций
docker-compose exec ${MARKETPLACE} alembic upgrade head

# удаление неиспользуемых образов
docker image prune -f
