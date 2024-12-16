import asyncio
import logging
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from src.codeforces_api import CodeforcesAPI
from src.db_manager import DBManager
from src.settings import db_name, host, password, port, user
from src.tg_bot.tg_bot import run_bot


def main():
    # Создание БД
    db_manager = DBManager()
    db_manager.create_database(user, password, host, port, db_name)

    # Создание таблиц
    db_manager.create_tables()

    # Загрузка информации о задачах из Codeforces API
    cf_api = CodeforcesAPI()
    cf_api.load_problems_info()

    # Заполнение таблиц данными из Codeforces API
    db_manager.insert_problems(cf_api.problems)
    db_manager.insert_problems_statistics(cf_api.problems_statistics)

    # Запуск Telegram бота
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
