import pytest

from src.utils import (check_tag, extract_number, translate_tag_to_en,
                       translate_tag_to_rus)


def test_extract_number():
    """Тестирует метод для извлечения числа из текста."""

    assert extract_number("Сложность задачи 2500") == 2500
    assert extract_number("Сложность задачи девятьсот") is None


def test_check_tag():
    """Тестирует метод для проверки наличия тега в списке тегов."""

    assert check_tag("СИСТЕМА непересекающихся множеств") is True
    assert check_tag("Несуществующий тег") is False


def test_translate_tag_to_en():
    """Тестирует метод для перевода тега с русского языка на английский."""

    assert translate_tag_to_en(["структуры данных"]) == ["data structures"]
    with pytest.raises(Exception) as e:
        translate_tag_to_en(["Несуществующий тег"])
    assert str(e.value) == "Такого тега нет."


def test_translate_tag_to_rus():
    """Тестирует метод для перевода тега с английского языка на русский."""

    assert translate_tag_to_rus("number theory") == "теория чисел"
    with pytest.raises(Exception) as e:
        translate_tag_to_rus("Несуществующий тег")
    assert str(e.value) == "Такого тега нет."
