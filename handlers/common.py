"""BookBot: /start, главное меню, /random"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data import get_random_book, GENRES

router = Router()

MAIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📚 Жанры", callback_data="genres"),
        InlineKeyboardButton(text="🔍 Поиск", callback_data="search_start"),
    ],
    [
        InlineKeyboardButton(text="🎲 Случайная книга", callback_data="random_book"),
        InlineKeyboardButton(text="❤️ Избранное", callback_data="favorites"),
    ],
])

WELCOME = (
    "👋 Привет! Я <b>📚 BookBot</b> — твой книжный помощник!\n\n"
    "Я помогу тебе:\n"
    "• Найти книгу по жанру или автору\n"
    "• Открыть для себя что-то новое\n"
    "• Сохранить избранные книги\n"
    "• Получить случайную рекомендацию\n\n"
    "Что интересует? 👇"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME, reply_markup=MAIN_KB)


@router.message(Command("random"))
async def cmd_random(message: Message):
    book = get_random_book()
    await message.answer(_book_card(book), reply_markup=_book_kb(book["id"]))


@router.callback_query(F.data == "main_menu")
async def cb_main(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME, reply_markup=MAIN_KB)


@router.callback_query(F.data == "random_book")
async def cb_random(callback: CallbackQuery):
    book = get_random_book()
    await callback.message.edit_text(
        "🎲 <b>Случайная книга для тебя:</b>\n\n" + _book_card(book),
        reply_markup=_book_kb(book["id"])
    )


def _book_card(book: dict) -> str:
    stars = "★" * int(book["rating"]) + ("½" if book["rating"] % 1 >= 0.5 else "")
    return (
        f"{book['emoji']} <b>{book['title']}</b>\n"
        f"✍️ {book['author']} · {book['year']} г.\n"
        f"📄 {book['pages']} страниц\n"
        f"⭐ {book['rating']} / 5.0\n\n"
        f"📝 {book['desc']}"
    )


def _book_kb(book_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❤️ В избранное", callback_data=f"fav_add_{book_id}"),
            InlineKeyboardButton(text="🎲 Ещё", callback_data="random_book"),
        ],
        [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
    ])
