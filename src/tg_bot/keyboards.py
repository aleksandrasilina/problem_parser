from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.tags import TAGS


def get_inline_kb():
    """Инлайн кнопки для стартового сообщения."""

    inline_kb_list = [
        [
            InlineKeyboardButton(
                text="Подобрать задачи", callback_data="get_problem_selection"
            )
        ],
        [
            InlineKeyboardButton(
                text="Найти конкретную задачу", callback_data="get_problem"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def get_rating_inline_kb():
    """Инлайн кнопки для выбора сложности задачи."""

    builder = ReplyKeyboardBuilder()
    for i in range(8, 36):
        builder.add(types.KeyboardButton(text=str(i * 100)))
    builder.adjust(5)

    return builder.as_markup(resize_keyboard=True)


def get_tags_inline_kb():
    """Инлайн кнопки для выбора темы задачи."""

    builder = ReplyKeyboardBuilder()
    for tag in TAGS:
        builder.add(types.KeyboardButton(text=f"{tag[1]}"))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
