import os

from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
