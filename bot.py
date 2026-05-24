import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import (add_product, get_user_products, delete_product)
from parser import get_ozon_product

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class AddProduct(StatesGroup):
    waiting_url = State()
    waiting_threshold = State()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для отслеживания цен на Ozon.\n\n"
        "📌 Команды:\n"
        "/add — добавить товар\n"
        "/list — мои товары\n"
        "/delete <id> — удалить товар")

@dp.message(Command("add"))
async def add_start(message: Message, state: FSMContext):
    await message.answer("🔗 Отправь ссылку на товар Ozon:")
    await state.set_state(AddProduct.waiting_url)

@dp.message(AddProduct.waiting_url)
async def add_url(message: Message, state: FSMContext):
    url = message.text.strip()
    if "ozon.ru" not in url:
        await message.answer("❌ Это не ссылка Ozon. Попробуй ещё раз:")
        return

    await message.answer("⏳ Получаю данные о товаре...")
    name, price = await get_ozon_product(url)

    if not price:
        await message.answer("❌ Не удалось получить цену.")
        await state.clear()
        return

    await state.update_data(url=url, name=name, price=price)
    await message.answer(
        f"✅ Товар: {name}\n💰 Цена: {price:.0f} ₽\n\n"
        f"При каком % снижения уведомить? (например: 10)")
    await state.set_state(AddProduct.waiting_threshold)

@dp.message(AddProduct.waiting_threshold)
async def add_threshold(message: Message, state: FSMContext):
    try:
        threshold = float(message.text.replace(",", ".").strip())
        if not 0 < threshold <= 99:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи число от 1 до 99")
        return

    data = await state.get_data()
    add_product(message.from_user.id, data["url"], data["name"], data["price"], threshold)

    await message.answer(
        f"✅ Товар добавлен!\n"
        f"📦 {data['name']}\n"
        f"💰 Цена: {data['price']:.0f} ₽\n"
        f"📉 Порог: -{threshold}%")
    await state.clear()

@dp.message(Command("list"))
async def list_products(message: Message):
    items = get_user_products(message.from_user.id)
    if not items:
        await message.answer("📭 Пока нет товаров.")
        return

    text = "📋 Твои товары:\n\n"
    for pid, name, init_p, last_p, thr in items:
        text += (
            f"🆔 {pid} | {name[:40]}\n"
            f"   Было: {init_p:.0f} ₽ | Сейчас: {last_p:.0f} ₽ | Порог: -{thr}%\n\n")
    await message.answer(text)

@dp.message(Command("delete"))
async def delete(message: Message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Используй: /delete <id>")
        return
    delete_product(int(parts[1]), message.from_user.id)
    await message.answer("🗑 Товар удалён.")


async def check_prices():
    logging.info("🔄 Проверка цен...")
    products = get_all_products()

    for prod in products:
        pid, user_id, url, name, init_price, last_price, threshold, notified = prod
        _, new_price = await get_ozon_product(url)
        if not new_price:
            continue
         
        discount = (init_price - new_price) / init_price * 100
        update_price(pid, new_price, notified=bool(notified))

if discount >= threshold and not notified:
            try:
                await bot.send_message(
                    user_id,
                    f"🔥 Скидка!\n\n"
                    f"📦 {name}\n"
                    f"💰 Было: {init_price:.0f} ₽\n"
                    f"💸 Сейчас: {new_price:.0f₽\n"
                    f"📉 -{discount:.1f}%\n\n"
                    f"🔗 {url}"
                )
                update_price(pid, new_price, notified=True)
            except Exception as e:
                logging.error(f"Ошибка отправки: {e}")v                 
        await asyncio.sleep(2)
