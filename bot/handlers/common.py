from random import choice
from asyncio import sleep

from aiogram import F, Router, Bot, html
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.states import GuessRandom
from data.data_fetcher import get_random
from keyboards.inline import (
    tenses_kb, finish_next_kb, links_kb, finish_kb, guess_kb
)
from common.text import (
    WELCOME, HELP, GUESS, FINISH, LINKS,
    UNKNOWN, GUESS_F, CHOOSE_FN, CHOOSE_GUESS
)
from common.stickers import sticker_ids


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

delay = 3


@router.message(StateFilter(None), CommandStart())
async def cmd_start_no_state(message: Message, bot: Bot):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Hi, <b>{message.from_user.first_name}</b>! 🤝\n{WELCOME}",
        reply_markup=guess_kb,
    )


@router.message(StateFilter(GuessRandom.guess_random), CommandStart())
async def cmd_start_guess_random_state(message: Message, bot: Bot):
    await message.delete()
    msg = await bot.send_message(
        chat_id=message.from_user.id,
        text=GUESS_F,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=msg.message_id,
    )


@router.message(StateFilter(GuessRandom.finish_next), CommandStart())
async def cmd_start_guess_random_state(message: Message, bot: Bot):
    await message.delete()
    msg = await bot.send_message(
        chat_id=message.from_user.id,
        text=CHOOSE_FN,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=msg.message_id,
    )


@router.message(Command("help"))
async def cmd_help_no_state(message: Message, bot: Bot):
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id, text=HELP)


@router.message(Command("author"))
async def cmd_author_no_state(message: Message, bot: Bot):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=LINKS,
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
        text=GUESS,
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"💬 <b>{html.quote(random_sentence['sentence'])}</b>",
        reply_markup=tenses_kb.as_markup(),
    )
    await state.set_state(GuessRandom.guess_random)


@router.message(StateFilter(GuessRandom.guess_random), Command("guess"))
async def cmd_guess_no_state(message: Message, bot: Bot):
    await message.delete()
    msg = await bot.send_message(
        chat_id=message.from_user.id,
        text=GUESS_F,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=msg.message_id,
    )


@router.message(StateFilter(GuessRandom.finish_next), Command("guess"))
async def cmd_guess_no_state(message: Message, bot: Bot):
    await message.delete()
    msg = await bot.send_message(
        chat_id=message.from_user.id,
        text=CHOOSE_FN,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=msg.message_id,
    )


@router.callback_query(StateFilter(None), F.data.in_(available_tenses))
async def tense_chosen_(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=CHOOSE_GUESS,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.guess_random), F.data.in_(available_tenses))
async def tense_chosen_(callback: CallbackQuery, state: FSMContext, bot: Bot):
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
            reply_markup=finish_next_kb.as_markup(),
        )
    else:
        await bot.edit_message_text(
            text=f"💬 <b>{html.quote(random_sentence['sentence'])}</b>\n\n🔴 <b>{available_tenses[callback.data]}</b>\nRight answer is <b>{available_tenses[random_sentence['tense']]}</b>",
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=finish_next_kb.as_markup(),
        )

    await state.set_state(GuessRandom.finish_next)
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.finish_next), F.data.in_(available_tenses))
async def tense_chosen_(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=CHOOSE_FN,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(None), F.data == "finish")
async def cmd_finish_finish_or_next_state(
    callback: CallbackQuery, bot: Bot
):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=CHOOSE_GUESS,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.guess_random), F.data == "finish")
async def cmd_finish_finish_or_next_state(
    callback: CallbackQuery, bot: Bot
):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=GUESS_F,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.finish_next), F.data == "finish")
async def cmd_finish_finish_or_next_state(
    callback: CallbackQuery, state: FSMContext, bot: Bot
):
    await state.clear()
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    sticker = await bot.send_sticker(
        chat_id=callback.from_user.id,
        sticker=choice(sticker_ids),
    )
    await sleep(1)
    await callback.message.answer(
        text=FINISH,
        reply_markup=finish_kb,
    )
    await sleep(4)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=sticker.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(None), F.data == "guess")
@router.callback_query(StateFilter(None), F.data == "guess_again")
async def cmd_guess_callback_no_state(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot
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
        text=GUESS,
    )
    await callback.message.answer(
        text=f"💬 <b>{html.quote(random_sentence['sentence'])}</b>",
        reply_markup=tenses_kb.as_markup(),
    )
    await state.set_state(GuessRandom.guess_random)
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.guess_random), F.data == "guess")
@router.callback_query(StateFilter(GuessRandom.guess_random), F.data == "guess_again")
async def cmd_guess_callback_guess_random_state(
    callback: CallbackQuery, bot: Bot
):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=GUESS_F,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.finish_next), F.data == "guess")
@router.callback_query(StateFilter(GuessRandom.finish_next), F.data == "guess_again")
async def cmd_guess_callback_finish_next_state(
    callback: CallbackQuery, bot: Bot
):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=CHOOSE_FN,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(F.data == "credits")
async def cmd_credits_no_state(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    await callback.message.answer(
        text=LINKS,
        reply_markup=links_kb,
    )
    await callback.answer()


@router.callback_query(StateFilter(None), F.data == "next")
async def cmd_next_guess_random_state(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=CHOOSE_GUESS,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.guess_random), F.data == "next")
async def cmd_next_guess_random_state(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    msg = await callback.message.answer(
        text=GUESS_F,
    )
    await sleep(delay)
    await bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=msg.message_id,
    )
    await callback.answer()


@router.callback_query(StateFilter(GuessRandom.finish_next), F.data == "next")
async def cmd_next_finish_next_state(
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
        reply_markup=tenses_kb.as_markup(),
    )
    await state.set_state(GuessRandom.guess_random)


@router.message()
async def delete_all_messages(message: Message, bot: Bot):
    # await message.delete()
    msg = await bot.send_message(
        chat_id=message.from_user.id,
        text=UNKNOWN,
        reply_to_message_id=message.message_id
    )
    await sleep(delay)
    await message.delete()
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=msg.message_id,
    )
