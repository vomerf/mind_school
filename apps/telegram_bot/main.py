import os

from httpx import AsyncClient, HTTPError
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
# from dotenv import load_dotenv
from apps.telegram_bot.logger import bot_logger
from apps.core.config import settings
# load_dotenv()

# Пока что мокаем пользователя
# TEST_USER_NAME = os.getenv("TEST_USER_NAME")
# API_URL = os.getenv("API_URL")
# BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


class EnterScore(StatesGroup):
    waiting_for_subject = State()
    waiting_for_score = State()


@dp.message(Command("start"))
async def start_handler(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/register")],
            [KeyboardButton(text="/enter_scores")],
            [KeyboardButton(text="/view_scores")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "Привет! Я помогу вести учёт оценок.\nВыберите действие:", reply_markup=kb
    )


@dp.message(Command("register"))
async def register_handler(message: Message):
    await message.answer("Введите свои ФИ (например: Иванов Иван):")


@dp.message(lambda m: " " in m.text and len(m.text.split()) == 2)
async def register_name(message: Message):
    last_name, name = message.text.split()
    async with AsyncClient() as client:
        resp = await client.post(
            f"{settings.API_URL}/register-pupil/", json={"name": name, "last_name": last_name}
        )
    if resp.status_code == 200:
        await message.answer("Вы успешно зарегистрированы ✅")
    else:
        await message.answer(f"Ошибка регистрации: {resp.text}")


@dp.message(Command("view_scores"))
async def view_scores_handler(message: Message):
    async with AsyncClient() as client:
        resp = await client.get(f"{settings.API_URL}/subjects/")
        subjects = resp.json()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=subj["name"], callback_data=f"view_subject:{subj['name']}"
                )
            ]
            for subj in subjects
        ]
    )
    await message.answer("Выберите предмет:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data.startswith("view_subject:"))
async def subject_chosen(call: CallbackQuery):
    subject_name = call.data.split(":")[1]

    async with AsyncClient() as client:
        resp = await client.get(f"{settings.API_URL}/scores/{subject_name}")

    if resp.status_code != 200:
        await call.message.answer("Не удалось получить оценки")
        return

    scores = resp.json()
    if not scores:
        await call.message.answer(f"Оценок по предмету {subject_name} пока нет.")
        return

    scores_text = "\n".join(
        f"- {score['score']} дата получения {score['date_entered']}" for score in scores
    )
    await call.message.answer(f"Оценки по предмету {subject_name}:\n{scores_text}")


@dp.message(Command("enter_scores"))
async def enter_scores_handler(message: Message, state: FSMContext):
    async with AsyncClient() as client:
        resp = await client.get(f"{settings.API_URL}/subjects/")
        subjects = resp.json()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=sub["name"], callback_data=f"enter_subject:{sub['id']}"
                )
            ]
            for sub in subjects
        ]
    )
    await message.answer("Выберите предмет:", reply_markup=kb)
    await state.set_state(EnterScore.waiting_for_subject)


@dp.callback_query(lambda c: c.data and c.data.startswith("enter_subject:"))
async def subject_chosen(call: CallbackQuery, state: FSMContext):
    subject_id = int(call.data.split(":")[1])
    await state.update_data(subject_id=subject_id)
    await call.message.answer("Введите оценку:")
    await state.set_state(EnterScore.waiting_for_score)


@dp.message(EnterScore.waiting_for_score)
async def score_received(message: Message, state: FSMContext):
    data = await state.get_data()
    subject_id = data["subject_id"]

    try:
        score = int(message.text)
    except ValueError:
        bot_logger.error(f"Пользователь ввел некорректное значение {message}")
        await message.answer("Пожалуйста, введи корректное число.")
        return

    async with AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.API_URL}/scores/",
                json={"subject_id": subject_id, "score": score, "user_id": settings.TEST_USER_ID},
                timeout=5.0
            )
            response.raise_for_status()
        except HTTPError as e:
            bot_logger.error(f"Ошибка запроса: {e}")
            await message.answer("Не удалось создать оценку ❌ Попробуй позже.")
            return
        except Exception as e:
            bot_logger.error(f"Ошибка: {e}")
            await message.answer("Произошла ошибка, попробуйте сделать запрос позже")
            return
    await message.answer("Оценка успешно сохранена ✅")
    await state.clear()


if __name__ == "__main__":
    bot_logger.info("Бот запущен")
    dp.run_polling(bot)
