"""
handlers/favorites.py — Избранные книги BookBot.

Данные хранятся в FSMContext под ключом FAV_KEY.
Структура: list[str] — список book_id добавленных книг.
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from data import get_book_by_id

router = Router()
FAV_KEY = "favorites"


async def get_favorites(state: FSMContext) -> list[str]:
    """Извлекает список ID избранных книг из FSMContext.

    Returns:
        Список book_id или пустой list, если избранное пусто.
    """
    data = await state.get_data()
    return data.get(FAV_KEY, [])


async def save_favorites(state: FSMContext, favs: list[str]) -> None:
    """Сохраняет список избранного в FSMContext.

    Args:
        state: Текущий FSM-контекст пользователя.
        favs: Список book_id для сохранения.
    """
    await state.update_data({FAV_KEY: favs})


@router.message(Command("favorites"))
async def cmd_favorites(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /favorites — показывает список избранных."""
    await _show_favorites(message, state, edit=False)


@router.callback_query(F.data == "favorites")
async def cb_favorites(callback: CallbackQuery, state: FSMContext) -> None:
    """Отображает избранное через inline-кнопку."""
    await _show_favorites(callback.message, state, edit=True)


async def _show_favorites(message: Message, state: FSMContext, edit: bool) -> None:
    """Выводит список избранных книг. Общая логика для cmd_favorites и cb_favorites.

    Args:
        message: Объект сообщения (Message), в которое отправить ответ.
        state: Текущий FSM-контекст пользователя.
        edit: True — отредактировать текущее, False — отправить новое.
    """
    favs = await get_favorites(state)

    if not favs:
        text = (
            "❤️ <b>Избранное</b>\n\n"
            "Ваш список пуст.\n\n"
            "Открывайте карточки книг и нажимайте ❤️ В избранное!"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Жанры", callback_data="genres")],
            [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
        ])
    else:
        lines = [f"❤️ <b>Избранное</b> ({len(favs)} книг)\n"]
        buttons = []
        for book_id in favs:
            book = get_book_by_id(book_id)
            if book:
                lines.append(f"{book['emoji']} {book['title']} — {book['author']}")
                buttons.append([
                    InlineKeyboardButton(
                        text=f"📖 {book['title']}",
                        callback_data=f"book_{book['id']}"
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"fav_remove_{book['id']}"
                    ),
                ])

        buttons.append([
            InlineKeyboardButton(text="🗑 Очистить всё", callback_data="fav_clear"),
            InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"),
        ])
        text = "\n".join(lines)
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    if edit:
        await message.edit_text(text, reply_markup=kb)
    else:
        await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.startswith("fav_add_"))
async def cb_fav_add(callback: CallbackQuery, state: FSMContext) -> None:
    """Добавляет книгу в избранное (callback: fav_add_<book_id>). Игнорирует дубликаты."""
    book_id = callback.data[8:]
    book = get_book_by_id(book_id)
    if not book:
        await callback.answer("Книга не найдена", show_alert=True)
        return

    favs = await get_favorites(state)
    if book_id in favs:
        await callback.answer("Уже в избранном! ❤️", show_alert=True)
        return

    favs.append(book_id)
    await save_favorites(state, favs)
    await callback.answer(f"❤️ «{book['title']}» добавлена в избранное!", show_alert=True)


@router.callback_query(F.data.startswith("fav_remove_"))
async def cb_fav_remove(callback: CallbackQuery, state: FSMContext) -> None:
    """Удаляет книгу из избранного (callback: fav_remove_<book_id>)."""
    book_id = callback.data[11:]
    favs = await get_favorites(state)
    if book_id in favs:
        favs.remove(book_id)
        await save_favorites(state, favs)
    await _show_favorites(callback.message, state, edit=True)


@router.callback_query(F.data == "fav_clear")
async def cb_fav_clear(callback: CallbackQuery, state: FSMContext) -> None:
    """Полностью очищает список избранного."""
    await save_favorites(state, [])
    await callback.message.edit_text(
        "🗑 Избранное очищено.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Жанры", callback_data="genres")],
            [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
        ])
    )
