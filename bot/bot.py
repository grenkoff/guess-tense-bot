import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats

from bot_instance import bot
from handlers import common  # , guess_random
from common.bot_cmds_list import private


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # await common.register_handers_common(common.router)
    dp.include_router(common.router)
    # dp.include_router(guess_random.router)

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
