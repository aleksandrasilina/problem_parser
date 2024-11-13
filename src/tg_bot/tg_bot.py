import os
import sys

from aiogram import Bot, Dispatcher, F, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from src.tg_bot.keyboards import (get_inline_kb, get_rating_inline_kb,
                                  get_tags_inline_kb)
from src.utils import check_tag, extract_number

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from src.db_manager import DBManager
from src.settings import TELEGRAM_TOKEN

dp = Dispatcher()
db_manager = DBManager()


class Form(StatesGroup):
    """Класс для определения состояний."""

    id = State()
    tags = State()
    rating = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """Хэндлер на команду /start."""

    await message.answer(
        f"Привет, {html.bold(message.from_user.first_name)}!\n"
        f"Это бот для подбора задач с сайта codeforces.com.\n"
        f"Ты хочешь посмотреть подборку задач или найти конкретную задачу?",
        reply_markup=get_inline_kb(),
    )


@dp.callback_query(F.data == "get_problem_selection")
async def send_problems_selection(call: CallbackQuery, state: FSMContext):
    """
    Сохраняет состояние Form.rating.
    Запрашивает у пользователя сложность задачи.
    """

    await state.set_state(Form.rating)
    await call.answer()
    await call.message.answer(
        "Укажи желаемую сложность задачи.\n"
        "Сложность находится в диапазоне от 800 до 3500 и кратна 100.\n"
        "Например, 900, 1500, 1700.",
        reply_markup=get_rating_inline_kb(),
    )


@dp.message(Form.rating)
async def process_rating(message: Message, state: FSMContext):
    """
    Сохраняет введенную пользователем сложность задач.
    Запрашивает у пользователя темы задачи.
    Сохраняет состояние Form.tags.
    """

    check_rating = extract_number(message.text)

    if (
        not check_rating
        or not 800 <= check_rating <= 3500
        or not check_rating % 100 == 0
    ):
        await message.reply(
            "Пожалуйста, введите корректную сложность задачи.\n"
            "Число должно быть кратно 100 и находится в диапазоне от 800 до 3500."
        )
        return

    await state.update_data(rating=message.text)
    await state.set_state(Form.tags)
    await message.answer(
        "Напиши желаемую тему задачи.", reply_markup=get_tags_inline_kb()
    )


@dp.message(Form.tags)
async def process_tags(message: Message, state: FSMContext):
    """
    Сохраняет введенные пользователем темы задачи.
    Отправляет пользователю подборку из 10 задач.
    """

    if not check_tag(message.text):
        await message.reply(
            "Такой темы нет. Пожалуйста, введите корректную тему задачи.\n"
        )
        return

    await state.update_data(tags=message.text)
    data = await state.get_data()
    problems_selection = db_manager.get_problems_selection(
        tag=[data.get("tags")], rating=data.get("rating")
    )

    if problems_selection:
        problems_to_send = [
            f"{num + 1}. {problem[0]} (ID: {problem[1]})"
            for num, problem in enumerate(problems_selection)
        ]

        await message.answer(
            f"Задачи, соответствующие выбранным параметрам:\n"
            f"{"\n".join(problems_to_send)}",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "К сожалению, задач, соответствующих выбранным параметрам, не найдено."
            "Попробуй изменить параметры запроса.",
            reply_markup=types.ReplyKeyboardRemove(),
        )


@dp.callback_query(F.data == "get_problem")
async def send_problem(call: CallbackQuery, state: FSMContext):
    """Сохраняет состояние Form.id. Запрашивает ID задачи."""

    await state.set_state(Form.id)
    await call.answer()
    await call.message.answer("Укажи ID задачи.")


@dp.message(Form.id)
async def process_id(message: Message, state: FSMContext):
    """
    Сохраняет введенные пользователем ключевые слова.
    Отправляет пользователю информацию о выбранной задаче.
    """

    await state.update_data(id=message.text)
    problem = db_manager.find_problem(message.text)
    if problem:
        await message.answer(problem)
    else:
        await message.answer(
            "К сожалению, такой задачи не найдено. Попробуй изменить запрос."
        )


async def run_bot():
    bot = Bot(
        token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)
