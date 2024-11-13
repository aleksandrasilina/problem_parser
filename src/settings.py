import os

from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
