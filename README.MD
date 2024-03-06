# CDO task
## Функционал
- pass

## Запуск контейнеров
Быстрый запуск:
```
bash build/marketplace.sh
```

## Миграции
Создание директории apps/alembic/versions/ и создание миграций. Потребуется ввести название миграции:
```
bash build/migrations_build.sh
```
Необходимо проверить сгенерированные миграции в директории apps/marketplace/alembic/versions/.
Применение миграций:
```
bash build/migrations_activate.sh
```

## Dev Requirements
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