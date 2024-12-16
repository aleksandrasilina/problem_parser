from unittest.mock import AsyncMock

import pytest
from aiogram import html, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from src.tg_bot.keyboards import get_inline_kb, get_rating_kb, get_tags_kb
from src.tg_bot.tg_bot import (command_start_handler, process_id,
                               process_rating, process_tags, send_problem,
                               send_problems_selection)
from tests.test_tg_bot.utils import TEST_USER, TEST_USER_CHAT


@pytest.mark.asyncio
async def test_command_start_handler():
    """Тестирует хэндлер на команду /start."""

    message = AsyncMock()
    await command_start_handler(message)

    message.answer.assert_called_with(
        f"Привет, {html.bold(message.from_user.first_name)}!\n"
        f"Это бот для подбора задач с сайта codeforces.com.\n"
        f"Ты хочешь посмотреть подборку задач или найти конкретную задачу?",
        reply_markup=get_inline_kb(),
    )


@pytest.mark.asyncio
async def test_send_problems_selection(bot, storage):
    """Тестирует функцию send_problems_selection."""

    call = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    await send_problems_selection(call=call, state=state)

    assert await state.get_state() == "Form:rating"
    call.message.answer.assert_called_with(
        "Укажи желаемую сложность задачи.\n"
        "Сложность находится в диапазоне от 800 до 3500 и кратна 100.\n"
        "Например, 900, 1500, 1700.",
        reply_markup=get_rating_kb(),
    )


@pytest.mark.asyncio
async def test_process_rating(bot, storage):
    """Тестирует функцию process_rating."""

    message = AsyncMock(text="900")
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    await process_rating(message, state)

    assert await state.get_data() == {"rating": "900"}
    assert await state.get_state() == "Form:tags"
    message.answer.assert_called_with(
        "Напиши желаемую тему задачи.", reply_markup=get_tags_kb()
    )


@pytest.mark.asyncio
async def test_process_rating_error(bot, storage):
    """Тестирует функцию process_rating в случае, когда пользователь ввел некорректное значение сложности."""

    message = AsyncMock(text="500")
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    await process_rating(message, state)

    assert await state.get_data() == {}
    assert await state.get_state() is None
    message.reply.assert_called_with(
        "Пожалуйста, введите корректную сложность задачи.\n"
        "Число должно быть кратно 100 и находится в диапазоне от 800 до 3500."
    )


@pytest.mark.asyncio
async def test_process_tags(
    bot, storage, delete_db_data, db_manager, problems, problems_statistics
):
    """Тестирует функцию process_tags."""

    message = AsyncMock(text="деревья")
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    db_manager.insert_problems(problems)
    db_manager.insert_problems_statistics(problems_statistics)
    await state.update_data(rating=1900)

    await process_tags(message, state)

    assert await state.get_data() == {"tags": "деревья", "rating": 1900}
    message.answer.assert_called_with(
        "Задачи, соответствующие выбранным параметрам:\n1. Кай и снежинки (ID: 685B)",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@pytest.mark.asyncio
async def test_process_tags_error(bot, storage):
    """Тестирует функцию process_tags в случае, когда пользователь ввел некорректное значение темы задачи."""

    message = AsyncMock(text="несуществующая тема")
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    await process_tags(message, state)

    assert await state.get_data() == {}
    assert await state.get_state() is None
    message.reply.assert_called_with(
        "Такой темы нет. Пожалуйста, введите корректную тему задачи."
    )


@pytest.mark.asyncio
async def test_process_tags_no_problems(bot, storage):
    """Тестирует функцию process_tags в случае, когда не нашлось подходящих запросу задач."""

    message = AsyncMock(text="битмаски")
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    await process_tags(message, state)

    assert await state.get_data() == {"tags": "битмаски"}
    assert await state.get_state() is None
    message.answer.assert_called_with(
        "К сожалению, задач, соответствующих выбранным параметрам, не найдено."
        "Попробуй изменить параметры запроса.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@pytest.mark.asyncio
async def test_send_problem(bot, storage):
    """Тестирует функцию send_problem."""

    call = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    await send_problem(call=call, state=state)

    assert await state.get_state() == "Form:id"
    call.message.answer.assert_called_with("Укажи ID задачи.")


@pytest.mark.asyncio
async def test_process_id(
    bot, storage, delete_db_data, db_manager, problems, problems_statistics
):
    """Тестирует функцию process_id."""

    message = AsyncMock(text="683J")
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    db_manager.insert_problems(problems)
    db_manager.insert_problems_statistics(problems_statistics)
    await process_id(message, state)

    assert await state.get_data() == {"id": "683J"}
    message.answer.assert_called_with(
        "ID: 683J\n"
        "Название: Герой с бомбами\n"
        "Сложность: 3000\n"
        "Темы: *особенный\n"
        "Количество решений: 545"
    )


@pytest.mark.asyncio
async def test_process_id_no_problem(bot, storage):
    """Тестирует функцию process_id."""

    message = AsyncMock(text="683A")
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id),
    )
    await state.clear()
    await process_id(message, state)

    assert await state.get_data() == {"id": "683A"}
    message.answer.assert_called_with(
        "К сожалению, такой задачи не найдено. Попробуй изменить запрос."
    )
