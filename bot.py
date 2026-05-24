from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

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
