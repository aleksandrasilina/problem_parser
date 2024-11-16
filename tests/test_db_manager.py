import pytest


@pytest.mark.usefixtures("delete_db_data")
class TestProblems:
    """Класс для тестирования БД."""

    def test_insert_problems(self, db_manager, problems):
        """Тестирует заполнение БД данными по задачам."""

        db_manager.insert_problems(problems)

        assert len(db_manager.list_problems()) == 2

    def test_insert_problems_statistics(
        self, db_manager, problems, problems_statistics
    ):
        """Тестирует заполнение БД данными по статистике задач."""

        db_manager.insert_problems(problems)
        db_manager.insert_problems_statistics(problems_statistics)

        assert len(db_manager.list_problems_statistics()) == 2

    def test_find_problem(self, db_manager, problems, problems_statistics):
        """Тестирует поиск задачи по ID."""

        db_manager.insert_problems(problems)
        db_manager.insert_problems_statistics(problems_statistics)

        assert db_manager.find_problem("685B") == (
            "ID: 685B\n"
            "Название: Кай и снежинки\n"
            "Сложность: 1900\n"
            "Темы: структуры данных, поиск в глубину и подобное, дп, деревья\n"
            "Количество решений: 383"
        )

    def test_get_problems_selection(self, db_manager, problems, problems_statistics):
        """Тестирует получение списка из 10 задач, удовлетворяющих переданным пользователем теме и сложности."""

        db_manager.insert_problems(problems)
        db_manager.insert_problems_statistics(problems)

        assert (
            db_manager.get_problems_selection(tag=["дп"], rating="1900")
            == "1. Кай и снежинки (ID: 685B)"
        )
