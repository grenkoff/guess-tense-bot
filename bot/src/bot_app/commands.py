from aiogram import types

from . import messages

from .app import dp

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(messages.WELCOME_MESSAGE)