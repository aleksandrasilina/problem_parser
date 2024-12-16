# Парсер задач с сайта [codeforces.com](https://codeforces.com/)

Парсер задач с сайта codeforces.com каждый час собирает данные о задачах и сохраняет их в
базу данных.
Telegram-бот для взаимодействия с пользователями, предоставляющий возможность подбора задач по сложности и темам и
поиска по ID.

## Содержание
- [Технологии](#технологии)
- [Запуск проекта](#запуск-проекта)
- [Запуск проекта в docker-контейнере](#запуск-проекта-в-docker-контейнере)
- [Тестирование](#тестирование)

## Технологии
- Python
- PostgreSQL
- SQLAlchemy
- Aiogram
- APScheduler
- Docker
- Docker Compose

## Запуск проекта

1. Клонируйте проект
```
git clone git@github.com:aleksandrasilina/problems_parser.git
```
2. Установите зависимости
```
pip install -r requirements.txt
```
3. Создайте файл .env в соответствии с шаблоном .env.sample
4.  Загрузка задач, сохранение в БД, запуск телеграм бота
```
python main.py
```
5.  Запуск периодических задач (каждый час) по загрузке задач с сайта и сохранения в БД
```
python src/periodic_tasks.py
```

## Запуск проекта в docker контейнере

1. Установите POSTGRES_HOST=db
2. 
```
docker-compose build
```
3.
```
docker-compose up
```

## Тестирование:
```
pytest
```
