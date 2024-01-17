from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

pr_si_button = KeyboardButton('/Pr_Si')
pr_co_button = KeyboardButton('/Pr_Co')
pr_pe_button = KeyboardButton('/Pr_Pe')
pr_pe_co_button = KeyboardButton('/Pr_Pe_Co')

inline_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(pr_si_button, pr_co_button, pr_pe_button, pr_pe_co_button)

# inline_button_present_simple = InlineKeyboardButton('Pr Si', callback_data='present_simple')
# inline_button_present_continuous = InlineKeyboardButton('Pr Co', callback_data='present_continuous')
# inline_button_present_perfect = InlineKeyboardButton('Pr Pe', callback_data='present_perfect')
# inline_button_present_perfect_continuous = InlineKeyboardButton('Pr Pe Co', callback_data='present_perfect_continuous')
# inline_button_past_simple = InlineKeyboardButton('Pa Si', callback_data='past_simple')
# inline_button_past_continuous = InlineKeyboardButton('Pa Co', callback_data='past_continuous')
# inline_button_past_perfect = InlineKeyboardButton('Pa Pe', callback_data='past_perfect')
# inline_button_past_perfect_continuous = InlineKeyboardButton('Pa Pe Co', callback_data='past_perfect_continuous')
# inline_button_future_simple = InlineKeyboardButton('Fu Si', callback_data='future_simple')
# inline_button_future_continuous = InlineKeyboardButton('Fu Co', callback_data='future_continuous')
# inline_button_future_perfect = InlineKeyboardButton('Fu Pe', callback_data='future_perfect')
# inline_button_future_perfect_continuous = InlineKeyboardButton('Fu Pe Co', callback_data='future_perfect_continuous')
# inline_button_future_simple_in_the_past = InlineKeyboardButton('Fu Si Pa', callback_data='future_simple_in_the_past')
# inline_button_future_continuous_in_the_past = InlineKeyboardButton('Fu Co Pa', callback_data='future_continuous_in_the_past')
# inline_button_future_perfect_in_the_past = InlineKeyboardButton('Fu Pe Pa', callback_data='future_perfect_in_the_past')
# inline_button_future_perfect_continuous_in_the_past = InlineKeyboardButton('FuPeCoPa', callback_data='future_perfect_continuous_in_the_past')

# inline_kb = InlineKeyboardMarkup()

# inline_kb.row(inline_button_present_simple, inline_button_present_continuous, inline_button_present_perfect, inline_button_present_perfect_continuous)\
#          .row(inline_button_past_simple, inline_button_past_continuous, inline_button_past_perfect, inline_button_past_perfect_continuous)\
#          .row(inline_button_future_simple, inline_button_future_continuous, inline_button_future_perfect, inline_button_future_perfect_continuous)\
#          .row(inline_button_future_simple_in_the_past, inline_button_future_continuous_in_the_past, inline_button_future_perfect_in_the_past, inline_button_future_perfect_continuous_in_the_past)
