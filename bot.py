import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
import config
import os
import json
from datetime import datetime

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return {}
    with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(subscribers, f, ensure_ascii=False, indent=2)  

buttons = [
    [KeyboardButton(text="Как стать волонтером?")],
    [KeyboardButton(text="Где мы в соцсетях?")],
    [KeyboardButton(text="Ближайшие события")],
    [KeyboardButton(text="Как подать заявку на часы?")],
    [KeyboardButton(text="Что такое волонтёрский слёт?")],
    [KeyboardButton(text="Как с нами связаться?")],
    [KeyboardButton(text="Подписаться на рассылку")],
    [KeyboardButton(text="Отписаться от рассылки")]
]
kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сайт", url="https://example.com")],
    [InlineKeyboardButton(text="Telegram", url="https://example.com")],
    [InlineKeyboardButton(text="VK", url="https://example.com")],
    [InlineKeyboardButton(text="OK", url="https://example.com")],
    [InlineKeyboardButton(text="Группа волонтёров", url="https://example.com")]
])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот волонтёрского проекта. Чем могу помочь?",
        reply_markup=kb
    )

@dp.message(lambda m: m.text == "Как стать волонтером?")
async def how_to_volunteer(message: types.Message):
    await message.answer(
        "<b>Как стать волонтером:</b>\n\n"
        "1. Свяжись с организаторами.\n"
        "2. Пройди обучающий тренинг.\n"
        "3. Участвуй в мероприятиях!\n\n"
        "Добро пожаловать ❤️"
    )

@dp.message(lambda m: m.text == "Где мы в соцсетях?")
async def socials(message: types.Message):
    await message.answer(
        "<b>Наши соцсети:</b>\n\n"
        "🔗 <a href='https://example.com'>VK</a>\n"
        "🔗 <a href='https://example.com'>Telegram</a>\n"
        "🔗 <a href='https://example.com'>ОК</a>\n"
        "🔗 <a href='https://example.com'>Сайт</a>\n",
        reply_markup=inline_kb
    )

@dp.message(lambda m: m.text == "Ближайшие события")
async def events(message: types.Message):
    try:
        path = os.path.join(os.path.dirname(__file__), "events.txt")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            await message.answer(f"<b>Ближайшие события:</b>\n\n{content}")
        else:
            await message.answer("Пока нет запланированных событий.")
    except FileNotFoundError:
        await message.answer("Файл с событиями не найден.")

@dp.message(lambda m: m.text == "Как подать заявку на часы?")
async def submit_hours(message: types.Message):
    await message.answer(
        "<b>Как подать заявку:</b>\n\n"
        "1. Зарегистрируйся на платформе.\n"
        "2. Найди мероприятие.\n"
        "3. Подай заявку и жди подтверждения."
    )

@dp.message(lambda m: m.text == "Что такое волонтёрский слёт?")
async def meeting(message: types.Message):
    await message.answer(
        "<b>Волонтёрский слёт</b> — это мероприятие для обмена опытом, мастер-классов и совместного отдыха!"
    )

@dp.message(lambda m: m.text == "Как с нами связаться?")
async def contact(message: types.Message):
    await message.answer(
        "<b>Контакты:</b>\n\n"
        "📱 Соцсети — <a href='https://example.com'>Группа ВК</a>"
    )

@dp.message(lambda m: m.text == "Подписаться на рассылку")
async def subscribe(message: types.Message):
    subscribers = load_subscribers()
    uid = str(message.from_user.id)
    if uid not in subscribers:
        subscribers[uid] = {
            "name": message.from_user.full_name,
            "status": "subscribed",
            "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        save_subscribers(subscribers)
        await message.answer("✅ Подписка оформлена!")
    else:
        subscribers[uid]["status"] = "subscribed"
        save_subscribers(subscribers)
        await message.answer("Подписка обновлена!")

@dp.message(lambda m: m.text == "Отписаться от рассылки")
async def unsubscribe(message: types.Message):
    subscribers = load_subscribers()
    uid = str(message.from_user.id)
    if uid in subscribers and subscribers[uid]["status"] == "subscribed":
        subscribers[uid]["status"] = "unsubscribed"
        save_subscribers(subscribers)
        await message.answer("❌ Ты отписан.")
    else:
        await message.answer("Ты не был подписан.")

@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id != config.ADMIN_ID:
        await message.answer("⛔ Нет доступа.")
        return

    text = message.text[len("/broadcast "):].strip()
    if not text:
        await message.answer("Добавь текст после команды.")
        return

    subscribers = load_subscribers()
    success, fail = 0, 0

    for uid, data in subscribers.items():
        if data.get("status") == "subscribed":
            try:
                await bot.send_message(uid, f"📢 <b>Новое сообщение:</b>\n\n{text}")
                success += 1
            except:
                fail += 1

    await message.answer(f"Готово.\n✅ Отправлено: {success}\n❌ Ошибок: {fail}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
