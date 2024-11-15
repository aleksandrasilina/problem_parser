from apscheduler.schedulers.blocking import BlockingScheduler

from src.codeforces_api import CodeforcesAPI
from src.db_manager import DBManager

scheduler = BlockingScheduler()
cf_api = CodeforcesAPI()
db_manager = DBManager()

# Запускает парсинг сайта codeforces.com и сохранение информации о проблемах в БД каждый час
scheduler.add_job(cf_api.load_problems_info, "interval", hours=1)
scheduler.add_job(
    db_manager.insert_problems, "interval", args=[cf_api.problems], hours=1
)
scheduler.add_job(
    db_manager.insert_problems_statistics,
    "interval",
    args=[cf_api.problems_statistics],
    hours=1,
)

scheduler.start()
