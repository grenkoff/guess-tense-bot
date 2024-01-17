from aiogram import types

from bot_app.states import GameStates
from aiogram.dispatcher import FSMContext
from . app import dp, bot
from . keyboards import inline_kb
from . data_fetcher import get_random

@dp.message_handler(commands='guess_ten', state='*')
async def  train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    res = await get_random()
    async with state.proxy() as data:
        data['step'] = 1
        data['answer'] = res.get('tense')
        data['sentence'] = res.get('sentence')
    
        await message.reply(f"{ data['step'] } of 10.\n{ data['sentence'] }", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data in ['Pr_Si', 'Pr_Co', 'Pr_Pe', 'Pr_Pe_Co', 'past_simple', 'past_continuous', 'past_perfect', 'past_perfect_continuous', 'future_simple', 'future_continuous', 'future_perfect', 'future_perfect_continuous', 'future_simple_in_the_past', 'future_continuous_in_the_past', 'future_perfect_in_the_past', 'future_perfect_continuous_in_the_past'], state=GameStates.random_ten)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    async with state.proxy() as data:
        if answer == data.get('answer'):
            res = await get_random()
            data['step'] += 1
            data['answer'] = res.get('tense')
            data['sentence'] = res.get('sentence')
            if data['step'] > 10:
                await bot.send_message(callback_query.from_user.id, "The game is over!!!")
                await GameStates.start.set()
            else:
                await bot.send_message(callback_query.from_user.id, 'Yes\n' + f"{ data['step'] } of 10.\n{ data['sentence'] }", reply_markup=inline_kb)
        else:
            await bot.send_message(callback_query.from_user.id, f'No\n', reply_markup=inline_kb)
