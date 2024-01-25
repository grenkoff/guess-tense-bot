from random import choice

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.methods.delete_message import DeleteMessage

# from bot_instance import bot
from utils.states import GuessRandom
from data.data_fetcher import get_random
from keyboards.reply import tenses_kb,finish_next_kb
from keyboards.inline import finish_or_next_kb, links_kb
from welcome import WELCOME, HELP


router = Router()

available_tenses = {
    "Pr Si": "Present Simple",
    "Pr Co": "Present Continuous",
    "Pr Pe": "Present Perfect",
    "Pr Pe Co": "Present Perfect Continuous",
    "Pa Si": "Past Simple",
    "Pa Co": "Past Continuous",
    "Pa Pe": "Past Perfect",
    "Pa Pe Co": "Past Perfect Continuous",
    "Fu Si": "Future Simple",
    "Fu Co": "Future Continuous",
    "Fu Pe": "Future Perfect",
    "Fu Pe Co": "Future Perfect Continuous",
}


@router.message(StateFilter(None), CommandStart())
async def cmd_start_no_state(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Hi, <b>{message.from_user.first_name}</b>! 🤝\n{WELCOME}",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(StateFilter("GuessRandom:guess_random"), CommandStart())
async def cmd_start_guess_random_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(StateFilter("GuessRandom:finish_or_next"), CommandStart())
async def cmd_start_finish_or_next_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"{HELP}"
    )


@router.message(Command("author"))
async def cmd_help(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"This bot was created by me 🙋‍♂️\n\nThere are my 🔗 links:",
        reply_markup=links_kb
    )


@router.message(StateFilter(None), Command("guess"))
@router.message(StateFilter("GuessRandom:finish_or_next"), Command("next"))
@router.message(StateFilter("GuessRandom:finish_or_next"), F.text.lower() == "next")
async def cmd_guess_no_state(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    global random_sentence
    # random_sentence = choice(tuple(sentences.keys()))
    random_sentence = await get_random()
    data = await state.get_data()
    data['answer'] = random_sentence.get('tense')
    data['sentence'] = random_sentence.get('sentence')
    await state.set_data(data)
    await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Guess the tense\n\n💬 <b>{random_sentence['sentence']}</b>",
            reply_markup=tenses_kb()
    )
    await state.set_state(GuessRandom.guess_random)


@router.message(StateFilter("GuessRandom.guess_random"), Command("guess"))
async def cmd_guess_guess_random_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(StateFilter("GuessRandom.finish_or_next"), Command("guess"))
async def cmd_guess_finish_or_next_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(StateFilter(None), Command("next"))
async def cmd_next_no_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(StateFilter("GuessRandom:guess_random"), Command("next"))
async def cmd_next_guess_random_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(StateFilter(None), Command("finish"))
async def cmd_finish_no_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(StateFilter("GuessRandom:guess_random"), Command("finish"))
async def cmd_finish_guess_random_state(message: Message, state: FSMContext):
    await message.delete()


@router.message(StateFilter("GuessRandom:finish_or_next"), Command("finish"))
@router.message(StateFilter("GuessRandom:finish_or_next"), F.text.lower() == "finish")
async def cmd_finish_finish_or_next_state(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await state.clear()
    await bot.send_message(
        chat_id=message.from_user.id,
        text="The game is over.\nSee you later 🖐\n\nOr use the /guess command to start the game again.", # должно быть сообщение о счете: Your Score is 18/20 or 90% correct answers.
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(GuessRandom.guess_random, F.text.in_(available_tenses))
async def tense_chosen(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await state.update_data(chosen_tense=message.text.lower())
    if message.text == random_sentence['tense']:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"✅ <b>{available_tenses[message.text]}</b>\nAnd it`s correct!",
            reply_markup=finish_next_kb()
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"🔴 <b>{available_tenses[message.text]}</b>\nRight answer is <b>{available_tenses[random_sentence['tense']]}</b>",
            reply_markup=finish_next_kb()
        )

    await state.set_state(GuessRandom.finish_or_next)


@router.message()
async def delete_all_messages(message: Message):
    await message.delete()
