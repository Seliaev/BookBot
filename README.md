# 📚 BookBot — Telegram Книжный Помощник

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://docs.aiogram.dev)

Демонстрационный Telegram-бот книжного помощника. 30+ книг по жанрам, случайная рекомендация, поиск и избранное — всё в одном боте.

🤖 **Демо-бот:** [@Portfolio_2_Book_Bot](https://t.me/Portfolio_2_Book_Bot)

---

## ✨ Возможности

- 📖 **Каталог книг** — 30+ книг, разбитых по жанрам (фантастика, детективы, классика, бизнес и др.)
- 🎲 **Случайная книга** — рекомендация по кнопке, если не знаете что читать
- 🔍 **Поиск** — по названию или автору
- ❤️ **Избранное** — сохранение понравившихся книг (per-user FSM)
- 📌 **Inline-режим** — поиск книг прямо в любом чате через `@bookbot запрос`

## 🛠 Стек

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.10+ |
| Фреймворк | aiogram 3.x |
| FSM Storage | MemoryStorage |
| Данные | Встроенный Python dict |
| Деплой | VPS / любой хостинг |

## 📁 Структура проекта

```
bookbot/
├── bot.py              # Точка входа, запуск polling
├── config.py           # Токен
├── data.py             # База книг (30+ записей)
├── handlers/
│   ├── common.py       # /start, главное меню
│   ├── catalog.py      # Жанры и список книг
│   ├── search.py       # Поиск по ключевому слову
│   └── favorites.py    # Избранное
└── requirements.txt
```

## 🚀 Запуск

```bash
git clone https://github.com/Seliaev/BookBot.git
cd BookBot
pip install -r requirements.txt
```

Создайте файл `.env` или отредактируйте `config.py`:

```python
BOT_TOKEN = "ваш_токен_от_BotFather"
```

```bash
python bot.py
```

## 💬 Команды

| Команда | Действие |
|---------|----------|
| `/start` | Главное меню |
| `/random` | Случайная книга |
| `/search текст` | Поиск книги |
| `/favorites` | Избранное |

## 📸 Демонстрация

Попробуйте бота прямо сейчас: [@Portfolio_2_Book_Bot](https://t.me/Portfolio_2_Book_Bot)

---

> Разработано [Denis Seliaev](https://github.com/Seliaev) · [Заказать похожий проект](https://kwork.ru/user/seliaev)
