"""
handlers/genres.py — Жанры и карточки книг BookBot.

Обрабатывает callback-и:
  genres         — список жанров
  genre_<key>    — книги выбранного жанра
  book_<id>      — карточка конкретной книги
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data import GENRES, BOOKS, get_book_by_id

router = Router()


def genres_kb() -> InlineKeyboardMarkup:
    """Клавиатура со списком всех доступных жанров."""
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"genre_{key}")]
        for key, name in GENRES.items()
    ]
    buttons.append([InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def books_list_kb(genre_key: str, books: list[dict]) -> InlineKeyboardMarkup:
    """Клавиатура со списком книг выбранного жанра.

    Args:
        genre_key: Ключ жанра (используется для кнопки «Назад»).
        books: Список словарей книг из data.BOOKS.
    """
    buttons = [
        [InlineKeyboardButton(
            text=f"{b['emoji']} {b['title']}",
            callback_data=f"book_{b['id']}"
        )]
        for b in books
    ]
    buttons.append([InlineKeyboardButton(text="◀️ Жанры", callback_data="genres")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def book_detail_kb(book_id: str, genre_key: str) -> InlineKeyboardMarkup:
    """Клавиатура карточки книги: в избранное, назад к жанру, главная.

    Args:
        book_id: Идентификатор книги.
        genre_key: Ключ жанра для кнопки «К списку».
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❤️ В избранное", callback_data=f"fav_add_{book_id}"),
        ],
        [
            InlineKeyboardButton(text="◀️ К списку", callback_data=f"genre_{genre_key}"),
            InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"),
        ],
    ])


def _get_genre_for_book(book_id: str) -> str | None:
    """Находит ключ жанра, к которому принадлежит книга.

    Args:
        book_id: Уникальный идентификатор книги.

    Returns:
        Ключ жанра из BOOKS или None, если книга не найдена.
    """
    for genre_key, books in BOOKS.items():
        for b in books:
            if b["id"] == book_id:
                return genre_key
    return None


@router.callback_query(F.data == "genres")
async def cb_genres(callback: CallbackQuery) -> None:
    """Показывает список жанров."""
    await callback.message.edit_text(
        "📚 <b>Жанры</b>\n\nВыберите интересующий жанр:",
        reply_markup=genres_kb()
    )


@router.callback_query(F.data.startswith("genre_") & ~F.data.startswith("genre_back"))
async def cb_genre(callback: CallbackQuery) -> None:
    """Показывает список книг выбранного жанра (callback: genre_<key>)."""
    genre_key = callback.data[6:]
    if genre_key not in BOOKS:
        await callback.answer("Жанр не найден")
        return

    books = BOOKS[genre_key]
    genre_name = GENRES[genre_key]
    await callback.message.edit_text(
        f"{genre_name}\n\n"
        f"Книг в жанре: <b>{len(books)}</b>\n"
        "Выберите книгу 👇",
        reply_markup=books_list_kb(genre_key, books)
    )


@router.callback_query(F.data.startswith("book_"))
async def cb_book_detail(callback: CallbackQuery) -> None:
    """Показывает карточку книги (callback: book_<id>)."""
    book_id = callback.data[5:]
    book = get_book_by_id(book_id)
    if not book:
        await callback.answer("Книга не найдена")
        return

    genre_key = _get_genre_for_book(book_id) or "classics"
    stars = "★" * int(book["rating"])
    text = (
        f"{book['emoji']} <b>{book['title']}</b>\n"
        f"✍️ {book['author']} · {book['year']} г.\n"
        f"📄 {book['pages']} страниц\n"
        f"⭐ {book['rating']} / 5.0\n\n"
        f"📝 {book['desc']}"
    )
    await callback.message.edit_text(text, reply_markup=book_detail_kb(book_id, genre_key))
