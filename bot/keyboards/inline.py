from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=agrenkoff"),
            InlineKeyboardButton(text="Github", url="https://github.com/grenkoff")
        ]
    ]
)

finish_or_next_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Finish", url="tg://resolve?domain=agrenkoff"),
            InlineKeyboardButton(text="Next", url="https://github.com/grenkoff/guess-tense-bot")
        ]
    ]
)
