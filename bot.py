import asyncio
import logging
import sys

# import httpx
from aiogram import Bot, types, Router, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from base import *

TOKEN = config('TOKEN')
# DEEPL_API_KEY = config('DEEPL_API_KEY')
ADMIN_ID = config('ADMIN_ID')

router = Router()


class AdminState(StatesGroup):
    waiting_for_choice = State()


# async def translate_text(text):
#     async with httpx.AsyncClient() as client:
#         url = "https://api.deepl.com/v2/translate"
#         params = {
#             "text": text,
#             "source_lang": "EN",  # Исходный язык - английский
#             "target_lang": "RU",  # Целевой язык - русский
#             "auth_key": DEEPL_API_KEY,
#         }
#         response = await client.post(url, data=params)
#         data = response.json()
#         if "translations" in data:
#             return data["translations"][0]["text"]
#         else:
#             return "Не удалось перевести текст"


async def fake_deepl_translation(text):
    # Функция выполняет фиктивный перевод текста
    translations = {'Hello': 'Привет',
                    'World': 'Мир',
                    "I couldn't register for Deepl from Russia": 'Я не смог зарегистрироваться в Deepl из России'}
    if text in translations:
        return translations[text]
    return "Error"


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик для комманды /start
    """
    user_id = message.from_user.id
    await message.answer("Привет!\nПопробуй ввести сообщение на английском")

    # Сохраняем пользователя в базу данных
    await add_user(user_id)


@router.message(Command("admin"))
async def admin(message: Message, state: FSMContext):
    """
    Обработчик для перехода в режим администратора
    """
    # Проверяем, что команду вызвал администратор (ваш Telegram ID)
    if message.from_user.id != int(ADMIN_ID):
        await message.answer(f"Вы не администратор {message.from_user.id}")
        return
    # Устанавливаем состояние ожидания
    await state.set_state(AdminState.waiting_for_choice)
    # Отправляем сообщение с инструкцией
    await message.answer("Для вывода всех записей о переводах, наберите - /all\n"
                         "Для вывода записей о переводах пользователя, наберите id пользователя\n"
                         "Для выхода из режима администратора, наберите - /exit")


@router.message(AdminState.waiting_for_choice)
async def admin(message: Message, state: FSMContext):
    """
    Обработчик для выбора действия у администратора
    """

    if message.text == "/all":
        ans = await get_all_translations()
        await message.answer(ans)
    elif message.text == "/exit":
        await state.clear()
    else:
        ans = await get_translations_by_user(int(message.text))
        await message.answer(ans)


@router.message()
async def translate_handler(message: types.Message):
    """
    Обработчик для перевода текста с английского на русский
    """
    text_to_translate = message.text
    user_id = message.from_user.id

    translated_text = await fake_deepl_translation(text_to_translate)

    # Отправляем переведенный текст пользователю
    await message.answer(translated_text, parse_mode=ParseMode.MARKDOWN)

    # Сохраняем запись о переводе в базу данных
    await add_translation(user_id, text_to_translate, translated_text)


async def main() -> None:
    # Создаём таблицы в бд, если их нет
    await create_users_table()
    await create_translations_table()

    # Запускаем бота
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
