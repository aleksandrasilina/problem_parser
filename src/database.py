from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import db_name, host, password, port, user

engine = create_engine(
    url=f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}",
    echo=True,
)


session_factory = sessionmaker(engine)
