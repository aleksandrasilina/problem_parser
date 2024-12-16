import pytest

from src.codeforces_api import CodeforcesAPI
from src.database import engine
from src.db_manager import DBManager
from src.models import Base, Problem, ProblemStatistics


@pytest.fixture
def cf_api():
    """Возвращает экземпляр класса CodeforcesAPI."""

    return CodeforcesAPI()


@pytest.fixture
def db_manager():
    """Возвращает экземпляр класса DBManager."""

    return DBManager()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Удаляет и создает таблицы в БД."""

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture
def delete_db_data(db_manager):
    """Удаляет  все данные из таблиц problems и problems_statistics."""

    db_manager.delete_all()


@pytest.fixture
def problems():
    """Возвращает список словарей с данными о задачах с API codeforces.com."""

    return [
        {
            "contestId": 685,
            "index": "B",
            "name": "Кай и снежинки",
            "type": "PROGRAMMING",
            "points": 1250.0,
            "rating": 1900,
            "tags": ["data structures", "dfs and similar", "dp", "trees"],
        },
        {
            "contestId": 683,
            "index": "J",
            "name": "Герой с бомбами",
            "type": "PROGRAMMING",
            "rating": 3000,
            "tags": ["*special"],
        },
    ]


@pytest.fixture
def problems_statistics():
    """Возвращает список словарей с данными о статистике по задачам с API codeforces.com."""

    return [
        {"contestId": 685, "index": "B", "solvedCount": 383},
        {"contestId": 683, "index": "J", "solvedCount": 545},
    ]


@pytest.fixture
def problem():
    """Возвращает экземпляр класса Problem."""

    problem_data = {
        "problem_id": "685B",
        "contest_id": 685,
        "name": "Кай и снежинки",
        "rating": 1900,
        "tags": ["data structures", "dfs and similar", "dp", "trees"],
    }
    return Problem(**problem_data)


@pytest.fixture
def problem_statistics():
    """Возвращает экземпляр класса ProblemStatistics."""

    problem_statistics_data = {
        "problem_id": "685B",
        "solved_count": 383,
    }
    return ProblemStatistics(**problem_statistics_data)
