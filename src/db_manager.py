import psycopg2
from sqlalchemy import delete, select

from src.database import engine, session_factory
from src.models import Base, Problem, ProblemStatistics
from src.utils import translate_tag_to_en, translate_tag_to_rus


class DBManager:
    """Класс для работы с postgresql."""

    @staticmethod
    def create_database(
        user: str, password: str, host: str, port: str, db_name: str
    ) -> None:
        """Создание базы данных для сохранения информации о задачах с сайта codeforces.com."""

        conn = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")

        conn.close()

    @staticmethod
    def create_tables() -> None:
        """Создание таблиц problems и problems_statistics для сохранения данных о задачах."""

        engine.echo = False
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.echo = True

    @staticmethod
    def insert_problems(problems: list[dict]) -> None:
        """Добавление данных о задачах из codeforces API в таблицу problems."""

        with session_factory() as session:
            problems_to_add = []
            for problem in problems:
                problems_to_add.append(
                    Problem(
                        problem_id=str(problem.get("contestId")) + problem.get("index"),
                        contest_id=problem.get("contestId"),
                        name=problem.get("name"),
                        rating=problem.get("rating"),
                        tags=problem.get("tags"),
                    )
                )
            session.add_all(problems_to_add)
            session.commit()

    @staticmethod
    def insert_problems_statistics(problems_statistics: list[dict]) -> None:
        """Добавление статистические данных о задачах из codeforces API в таблицу problems_statistics."""

        with session_factory() as session:
            problems_statistics_to_add = [
                ProblemStatistics(
                    problem_id=str(problem_statistics.get("contestId"))
                    + problem_statistics.get("index"),
                    solved_count=problem_statistics.get("solvedCount"),
                )
                for problem_statistics in problems_statistics
            ]

            session.add_all(problems_statistics_to_add)
            session.commit()

    @staticmethod
    def find_problem(entered_id: str) -> str:
        """
        Поиск задачи по переданным пользователем ключевым словам.
        Если задач несколько, то возвращает информацию по случайной задаче.
        """

        with session_factory() as session:
            query = (
                session.query(Problem, ProblemStatistics)
                .filter(Problem.problem_id == entered_id)
                .join(
                    ProblemStatistics,
                    Problem.problem_id == ProblemStatistics.problem_id,
                )
            )
            problem = query.all()
            if problem:
                return (
                    f"ID: {problem[0][0].problem_id}\n"
                    f"Название: {problem[0][0].name}\n"
                    f"Сложность: {problem[0][0].rating}\n"
                    f"Темы: {", ".join([translate_tag_to_rus(tag) for tag in problem[0][0].tags])}\n"
                    f"Количество решений: {problem[0][1].solved_count}"
                )

    @staticmethod
    def get_problems_selection(tag: list[str], rating: str) -> str:
        """
        Получение списка из 10 задач, удовлетворяющих переданным пользователем теме и сложности.
        При этом задачи не пересекаются между различными контестами.
        """

        with session_factory() as session:
            en_tag = translate_tag_to_en(tag)
            query = (
                session.query(Problem)
                .filter(Problem.rating == rating)
                .filter(Problem.tags.contains(en_tag))
                .distinct(Problem.contest_id)
                .limit(10)
            )
            problem_objects = query.all()
            if problem_objects:
                return "\n".join(
                    [
                        f"{num + 1}. {problem.name} (ID: {problem.problem_id})"
                        for num, problem in enumerate(problem_objects)
                    ]
                )

    @staticmethod
    def list_problems():
        """Вывод всех задач из таблицы problems."""

        query = select(Problem)
        with session_factory() as session:
            problems = session.execute(query)
            session.commit()
            return problems.all()

    @staticmethod
    def list_problems_statistics():
        """Вывод всех задач из таблицы problems_statistics."""

        query = select(ProblemStatistics)
        with session_factory() as session:
            problems_statistics = session.execute(query)
            session.commit()
            return problems_statistics.all()

    @staticmethod
    def delete_all():
        """Удаление всех данных из таблиц problems и problems_statistics."""

        with session_factory() as session:
            session.execute(delete(ProblemStatistics))
            session.execute(delete(Problem))
            session.commit()
