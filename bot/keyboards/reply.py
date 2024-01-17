from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder

def tenses_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    pr_si = KeyboardButton(text="Pr Si")
    pr_co = KeyboardButton(text="Pr Co")
    pr_pe = KeyboardButton(text="Pr Pe")
    pr_pe_co = KeyboardButton(text="Pr Pe Co")
    pa_si = KeyboardButton(text="Pa Si")
    pa_co = KeyboardButton(text="Pa Co")
    pa_pe = KeyboardButton(text="Pa Pe")
    pa_pe_co = KeyboardButton(text="Pa Pe Co")
    fu_si = KeyboardButton(text="Fu Si")
    fu_co = KeyboardButton(text="Fu Co")
    fu_pe = KeyboardButton(text="Fu Pe")
    fu_pe_co = KeyboardButton(text="Fu Pe Co")

    kb.row(pr_si, pr_co, pr_pe, pr_pe_co)\
      .row(pa_si, pa_co, pa_pe, pa_pe_co)\
      .row(fu_si, fu_co, fu_pe, fu_pe_co)

    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Choose the correct tense"
    )


def finish_next_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    finish_b = KeyboardButton(text="Finish")
    next_b = KeyboardButton(text="Next")

    kb.row(finish_b, next_b)

    return kb.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Select Finish or Next"
    )
