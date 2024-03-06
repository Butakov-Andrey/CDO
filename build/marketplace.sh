#!/bin/bash

# определение .env файла
export ENV_FILE=./.env

# Остановка и удаление контейнеров
docker-compose down

# Запуск новых контейнеров 
docker-compose up -d --build

# удаление неиспользуемых образов
docker image prune -f
