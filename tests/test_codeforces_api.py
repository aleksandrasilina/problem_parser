import pytest


def test_codeforces_api_init(cf_api):
    """Тестирует конструктор для codeforces.com API."""

    assert cf_api.codeforces_api_url == "https://codeforces.com/api/"
    assert cf_api.codeforces_api_method == "problemset.problems"
    assert cf_api.problems == []
    assert cf_api.problems_statistics == []


def test_load_problems_info(cf_api):
    """Тестирует метод для загрузки информации о задачах и статистике по ним."""

    cf_api.load_problems_info()
    assert len(cf_api.problems) > 0
    assert len(cf_api.problems_statistics) > 0


def test_load_problems_info_failed_status(requests_mock, cf_api):
    """Тестирует исключение для загрузки информации о задачах."""

    data = {"status": "FAILED", "comment": "Call limit exceeded", "result": ""}
    requests_mock.register_uri(
        "GET", "https://codeforces.com/api/problemset.problems?lang=ru", json=data
    )
    with pytest.raises(Exception) as e:
        cf_api.load_problems_info()

    assert (
        str(e.value) == "Ошибка при загрузке информации о задачах: Call limit exceeded"
    )
