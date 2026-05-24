from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

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
