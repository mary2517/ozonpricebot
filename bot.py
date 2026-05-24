from aiogram.filters import CommandStart, Command
from aiogram.types import Message

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для отслеживания цен на Ozon.\n\n"
        "📌 Команды:\n"
        "/add — добавить товар\n"
        "/list — мои товары\n"
        "/delete <id> — удалить товар")
