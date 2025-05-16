import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
import os
from datetime import datetime

# Настройка бота
import config
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Клавиатура (основная)
buttons = [
    [KeyboardButton(text="Как стать волонтером СПИД-центра?")],
    [KeyboardButton(text="В каких социальных сетях мы есть?")],
    [KeyboardButton(text="Ближайшие акции")],
    [KeyboardButton(text="Как правильно подавать заявку на волонтерские часы?")],
    [KeyboardButton(text="Что такое слёт волонтеров?")],
    [KeyboardButton(text="Как с нами связаться?")]
]
kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Клавиатура WebApp (инлайн-кнопки)
inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Официальный сайт", url="https://aids-buryatia.ru")],
    [InlineKeyboardButton(text="Наш Telegram-канал", url="https://t.me/spidcentr03")],
    [InlineKeyboardButton(text="Мы в VK", url="https://vk.com/spidcentr03")],
    [InlineKeyboardButton(text="Мы в ОК", url="https://ok.ru/group/61341134618692")],
    [InlineKeyboardButton(text="Наша группа волонтёров в VK", url="https://vk.com/volonter_spidcentr03")]
])

# Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот волонтёрского движения СПИД-центра Бурятии. Чем могу помочь?",
        reply_markup=kb
    )

# Информационные кнопки
@dp.message(lambda m: m.text == "Как стать волонтером СПИД-центра?")
async def how_to_volunteer(message: types.Message):
    await message.answer(
        "<b>Как стать волонтером СПИД-центра:</b>\n\n"
        "1. Попроси руководство школы связаться с нами.\n"
        "2. Пройди тренинг «Равный обучает Равного».\n"
        "3. Приходи на акции!\n\n"
        "Добро пожаловать ❤️"
    )

@dp.message(lambda m: m.text == "В каких социальных сетях мы есть?")
async def socials(message: types.Message):
    await message.answer(
        "<b>Мы в соцсетях:</b>\n\n"
        "🔗 <a href='https://vk.com/spidcentr03'>ВКонтакте</a>\n"
        "🔗 <a href='https://ok.ru/group/61341134618692'>Одноклассники</a>\n"
        "🔗 <a href='https://t.me/spidcentr03'>Telegram-канал</a>\n"
        "🔗 <a href='https://vk.com/volonter_spidcentr03'>Группа волонтёров</a>\n"
        "🔗 <a href='https://aids-buryatia.ru'>Официальный сайт</a>",
        reply_markup=inline_kb
    )

@dp.message(lambda m: m.text == "Ближайшие акции")
async def events(message: types.Message):
    try:
        path = os.path.join(os.path.dirname(__file__), "events.txt")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            await message.answer(f"<b>Ближайшие акции:</b>\n\n{content}")
        else:
            await message.answer("Пока нет запланированных акций.")
    except FileNotFoundError:
        await message.answer("Файл с акциями не найден.")

@dp.message(lambda m: m.text == "Как правильно подавать заявку на волонтерские часы?")
async def submit_hours(message: types.Message):
    await message.answer(
        "<b>Как подать заявку на волонтерские часы:</b>\n\n"
        "1. Зайди на dobro.ru\n"
        "2. Найди нужное мероприятие\n"
        "3. Подай заявку и дождись подтверждения"
    )

@dp.message(lambda m: m.text == "Что такое слёт волонтеров?")
async def meeting(message: types.Message):
    await message.answer(
        "<b>Слёт волонтеров</b> — это ежегодное мероприятие, где волонтеры обмениваются опытом, участвуют в мастер-классах, обсуждают планы и просто классно проводят время вместе на Байкале!"
    )

@dp.message(lambda m: m.text == "Как с нами связаться?")
async def contact(message: types.Message):
    await message.answer(
        "<b>Связаться с нами:</b>\n\n"
        "📞 Телефон: +7 (3012) 46-11-55\n"
        "📱 Соцсети — <a href='https://vk.com/volonter_spidcentr03'>Наша группа волонтёров в ВК</a>"
    )

# Отправка фото (пример кнопки или команды для триггера)
@dp.message(Command("photo"))
async def send_photo(message: types.Message):
    path = os.path.join(os.path.dirname(__file__), "photo.jpg")  # Название фото
    if os.path.exists(path):
        photo = FSInputFile(path)
        await message.answer_photo(photo, caption="Вот фотография с последнего мероприятия!")
    else:
        await message.answer("Фото не найдено.")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
