"""
handlers/search.py — Поиск книг BookBot.

Поддерживает FSM-состояние SearchState.waiting_query для
получения поискового запроса от пользователя.
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data import search_books, get_book_by_id

router = Router()


class SearchState(StatesGroup):
    """FSM-состояния поиска."""

    waiting_query = State()


@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /search — запускает режим ожидания запроса."""
    await state.set_state(SearchState.waiting_query)
    await message.answer(
        "🔍 <b>Поиск книги</b>\n\n"
        "Введите название книги или имя автора:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="search_cancel")]
        ])
    )


@router.callback_query(F.data == "search_start")
async def cb_search_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Запускает поиск через inline-кнопку."""
    await state.set_state(SearchState.waiting_query)
    await callback.message.edit_text(
        "🔍 <b>Поиск книги</b>\n\n"
        "Введите название книги или имя автора:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="search_cancel")]
        ])
    )


@router.message(SearchState.waiting_query)
async def process_search(message: Message, state: FSMContext) -> None:
    """Обрабатывает запрос и выводит результаты. Максимум 8 совпадений."""
    query = message.text.strip()
    if len(query) < 2:
        await message.answer("❌ Слишком короткий запрос. Введите минимум 2 символа:")
        return

    await state.clear()
    results = search_books(query)

    if not results:
        await message.answer(
            f"🔍 По запросу «<b>{query}</b>» ничего не найдено.\n\n"
            "Попробуйте другое название или автора.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔍 Искать снова", callback_data="search_start")],
                [InlineKeyboardButton(text="📚 Жанры", callback_data="genres")],
                [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
            ])
        )
        return

    buttons = [
        [InlineKeyboardButton(
            text=f"{b['emoji']} {b['title']} — {b['author']}",
            callback_data=f"book_{b['id']}"
        )]
        for b in results[:8]  # максимум 8 результатов
    ]
    buttons.append([InlineKeyboardButton(text="🔍 Новый поиск", callback_data="search_start")])
    buttons.append([InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")])

    await message.answer(
        f"🔍 Результаты поиска «<b>{query}</b>»\n"
        f"Найдено: {len(results)} книг",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@router.callback_query(F.data == "search_cancel")
async def cb_search_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """Отменяет текущий поиск, сбрасывает FSM-состояние."""
    await state.clear()
    await callback.message.edit_text(
        "Поиск отменён.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")]
        ])
    )
