import requests


class CodeforcesAPI:
    """Класс для работы с codeforces.com API."""

    def __init__(self):
        self.__codeforces_api_url = (
            "https://codeforces.com/api/"  # url для запроса данных
        )
        self.__codeforces_api_method = "problemset.problems"  # метод запроса
        self.__problems = []  # список задач из архива codeforces.com
        self.__problems_statistics = (
            []
        )  # список статистических данных по задачам codeforces.com

    def load_problems_info(self) -> None:
        """Загружает информацию о задачах и статистику по ним."""

        response = requests.get(
            f"{self.__codeforces_api_url}{self.__codeforces_api_method}?lang=ru"
        ).json()

        if response["status"] == "OK":
            self.__problems = response["result"]["problems"]
            self.__problems_statistics = response["result"]["problemStatistics"]
        else:
            raise Exception(
                f"Ошибка при загрузке информации о задачах: {response['comment']}"
            )

    @property
    def codeforces_api_url(self) -> str:
        """Геттер для url codeforces.com API."""

        return self.__codeforces_api_url

    @property
    def problems(self) -> list[dict]:
        """Геттер для списка задач из архива сайта."""

        return self.__problems

    @property
    def codeforces_api_method(self) -> str:
        """Геттер для метода запроса."""

        return self.__codeforces_api_method

    @property
    def problems_statistics(self) -> list[dict]:
        """Геттер для вывода списка статистических данных по задачам из архива сайта."""

        return self.__problems_statistics
