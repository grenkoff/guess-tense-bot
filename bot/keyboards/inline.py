from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=agrenkoff"),
            InlineKeyboardButton(
                text="Github", url="https://github.com/grenkoff/guess-tense-bot"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Buy me a coffee ☕",
                web_app=WebAppInfo(url="https://www.buymeacoffee.com/grenkoff"),
            )
        ],
    ]
)

finish_next_kb = InlineKeyboardBuilder()
finish_b = InlineKeyboardButton(text="Finish 🏁", callback_data="finish")
next_b = InlineKeyboardButton(text="Next 👉", callback_data="next")
finish_next_kb.row(finish_b, next_b)


tenses_kb = InlineKeyboardBuilder()
pr_si = InlineKeyboardButton(text="Pr Si", callback_data="Pr Si")
pr_co = InlineKeyboardButton(text="Pr Co", callback_data="Pr Co")
pr_pe = InlineKeyboardButton(text="Pr Pe", callback_data="Pr Pe")
pr_pe_co = InlineKeyboardButton(text="Pr Pe Co", callback_data="Pr Pe Co")
pa_si = InlineKeyboardButton(text="Pa Si", callback_data="Pa Si")
pa_co = InlineKeyboardButton(text="Pa Co", callback_data="Pa Co")
pa_pe = InlineKeyboardButton(text="Pa Pe", callback_data="Pa Pe")
pa_pe_co = InlineKeyboardButton(text="Pa Pe Co", callback_data="Pa Pe Co")
fu_si = InlineKeyboardButton(text="Fu Si", callback_data="Fu Si")
fu_co = InlineKeyboardButton(text="Fu Co", callback_data="Fu Co")
fu_pe = InlineKeyboardButton(text="Fu Pe", callback_data="Fu Pe")
fu_pe_co = InlineKeyboardButton(text="Fu Pe Co", callback_data="Fu Pe Co")
tenses_kb.row(pr_si, pr_co, pr_pe, pr_pe_co)\
         .row(pa_si, pa_co, pa_pe, pa_pe_co)\
         .row(fu_si, fu_co, fu_pe, fu_pe_co)


finish_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Guess again", callback_data="guess_again"),
            InlineKeyboardButton(text="Credits 🙎‍♂️", callback_data="credits",)
        ]
    ]
)

guess_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Guess the tense 👉", callback_data="guess")]
    ]
)
