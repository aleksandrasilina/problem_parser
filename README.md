# Парсер задач с сайта [codeforces.com](https://codeforces.com/)

<hr>
Парсер задач с сайта [codeforces.com](https://codeforces.com/) каждый час собирает данные о задачах и сохраняет их в базу данных.
Telegram-бот для взаимодействия с пользователями, предоставляющий возможность подбора задач по сложности и темам и поиска по ID.

## Запуск проекта
1. Создайте файл .env в соответствии с шаблоном .env.sample
2. python main.py - загрузка задач, сохранение в БД, запуск телеграм бота
3. python src/periodic_tasks.py - запуск периодических задач (каждый час) по загрузке задач с сайта и сохранения в БД

## Запуск проекта в docker контейнере
1. POSTGRES_HOST=db
2. docker-compose build
3. docker-compose up

## Тестирование:
python manage.py test