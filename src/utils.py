import re

from src.tags import TAGS


def extract_number(text: str) -> int | None:
    """Извлекает число из текста."""

    match = re.search(r"\b(\d+)\b", text)
    if match:
        return int(match.group(1))
    else:
        return None


def check_tag(user_tag: str) -> bool:
    """Проверяет наличие тега в списке тегов."""

    for tag in TAGS:
        if tag[1] == user_tag.lower():
            return True
    return False


def translate_tag_to_en(rus_tag: list[str]) -> list[str]:
    """Переводит тег с русского языка на английский."""

    for tag in TAGS:
        if tag[1] == rus_tag[0].lower():
            return [tag[0]]


def translate_tag_to_rus(en_tag: str) -> str:
    """Переводит тег с английского языка на русский."""

    for tag in TAGS:
        if tag[0] == en_tag.lower():
            return tag[1]
