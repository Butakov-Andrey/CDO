# CDO task

API: http://127.0.0.1:8000/docs

Для запуска требуется .env файл в корне проекта.
Для получения .env файла - ([imblackmamba](https://t.me/imblackmamba13))

## Функционал
Products:
- crud для создания продукта
- получения списка продуктов в csv
- получени отзывов на продукт
Feedback:
- создание отзывов для продуктов, текст
- создание отзывов для продуктов, изображения (Tesseract)
- определение тона(настроения) отзыва (Mixtral)

## Запуск контейнеров
Быстрый запуск:
```
bash build/marketplace.sh
```

## Миграции
Создание директории apps/marketplace/alembic/versions/ и создание миграций. Потребуется ввести название миграции:
```
bash build/migrations_build.sh
```
Необходимо проверить сгенерированные миграции в директории apps/marketplace/alembic/versions/.
Применение миграций:
```
bash build/migrations_activate.sh
```

## Локальные зависимости для разработки
Для локальной установки зависимостей, запустите следующие команды:
```
pip install pip-tools
```

### Marketplace
```
pip-compile ./apps/marketplace/requirements.in
pip-sync ./apps/marketplace/requirements.txt
```

### Pre-commit
Установка pre-commit:
```
pre-commit install
```
[Указание директории](.pre-commit-config.yaml) в которых должны/не должны сработать pre-commit hooks:  
```
files: ^(apps/)
exclude: (?x).*/alembic($|/.*)
```