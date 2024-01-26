from aiogram import F, Router, Bot, html
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from utils.states import GuessRandom
from data.data_fetcher import get_random
from keyboards.inline import tenses_inline_kb, finish_or_next_kb, links_kb
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
async def cmd_start_no_state(message: Message, bot: Bot):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Hi, <b>{message.from_user.first_name}</b>! 🤝\n{WELCOME}",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(StateFilter(None), Command("help"))
async def cmd_help(message: Message, bot: Bot):
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id, text=f"{HELP}")


@router.message(StateFilter(None), Command("author"))
async def cmd_author(message: Message, bot: Bot):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"This bot was created by me 🙋‍♂️\n\nThere are my 🔗 links:",
        reply_markup=links_kb,
    )


@router.message(StateFilter(None), Command("guess"))
async def cmd_guess_no_state(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    global random_sentence
    random_sentence = await get_random()
    data = await state.get_data()
    data["answer"] = random_sentence.get("tense")
    data["sentence"] = random_sentence.get("sentence")
    await state.set_data(data)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Guess the tense 👇",
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"💬 <b>{html.quote(random_sentence['sentence'])}</b>",
        reply_markup=tenses_inline_kb.as_markup(),
    )
    await state.set_state(GuessRandom.guess_random)


@router.message(StateFilter("GuessRandom.guess_random"), Command("guess"))
async def cmd_guess_guess_random_state(message: Message):
    await message.delete()


@router.message(StateFilter("GuessRandom.finish_or_next"), Command("guess"))
async def cmd_guess_finish_or_next_state(message: Message):
    await message.delete()


@router.message()
async def delete_all_messages(message: Message):
    await message.delete()


@router.callback_query(F.data.in_(available_tenses))
async def tense_chosen(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(chosen_tense=callback.data.lower())
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    if callback.data == random_sentence["tense"]:
        await bot.edit_message_text(
            text=f"💬 <b>{html.quote(random_sentence['sentence'])}</b>\n\n✅ <b>{available_tenses[callback.data]}</b>\nAnd it`s correct!",
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=finish_or_next_kb.as_markup(),
        )
    else:
        await bot.edit_message_text(
            text=f"💬 <b>{html.quote(random_sentence['sentence'])}</b>\n\n🔴 <b>{available_tenses[callback.data]}</b>\nRight answer is <b>{available_tenses[random_sentence['tense']]}</b>",
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=finish_or_next_kb.as_markup(),
        )

    await state.set_state(GuessRandom.finish_or_next)
    await callback.answer()


@router.callback_query(F.data == "finish")
async def cmd_finish_finish_or_next_state(
    callback: CallbackQuery, state: FSMContext, bot: Bot
):
    await state.clear()
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    await callback.message.answer(
        text="The game is over 🏁\nSee you later 🖐\n\nOr use the /guess command to start the game again. ", # должно быть сообщение о счете: Your Score is 18/20 or 90% correct answers.
        reply_markup=ReplyKeyboardRemove(),
    )
    await callback.answer()


@router.callback_query(F.data == "next")
async def cmd_next_finish_or_next_state(
    callback: CallbackQuery, state: FSMContext, bot: Bot
):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    global random_sentence
    random_sentence = await get_random()
    data = await state.get_data()
    data["answer"] = random_sentence.get("tense")
    data["sentence"] = random_sentence.get("sentence")
    await state.set_data(data)
    await callback.message.answer(
        text=f"💬 <b>{html.quote(random_sentence['sentence'])}</b>",
        reply_markup=tenses_inline_kb.as_markup(),
    )
    await state.set_state(GuessRandom.guess_random)
