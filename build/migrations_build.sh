#!/bin/bash
MARKETPLACE=marketplace

export ENV_FILE=./.env

echo -n "Введите сообщение для миграции: "
read migration_message

docker-compose exec ${MARKETPLACE} alembic revision --autogenerate -m "$migration_message"