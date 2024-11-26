def test_problem_repr(problem):
    """Тестирует метод __repr__ класса Problem."""

    assert repr(problem) == "Кай и снежинки (ID: 685B)"


def test_problem_statistics_repr(problem_statistics):
    """Тестирует метод __repr__ класса ProblemStatistics."""

    assert repr(problem_statistics) == "Количество решений: 383 (ID: 685B)"
