#!/bin/bash
MARKETPLACE=marketplace

# определение .env файла
export ENV_FILE=./.env

# Запуск миграций
docker-compose exec ${MARKETPLACE} alembic upgrade head