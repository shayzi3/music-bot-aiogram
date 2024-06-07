import asyncio
import os

from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher

from callbacks import callback_find
from handlers.user_commands import start_, find
from handlers.bot_commands import messages

load_dotenv()

async def main() -> None:
     bot = Bot(os.getenv('TOKEN'))
     dp = Dispatcher()
     
     logger.info('Bot ready!')
     
     dp.include_routers(
          callback_find.router,
          start_.router,
          find.router,
          messages.router
     )
     
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)
     
     
if __name__ == '__main__':
     asyncio.run(main())
     
     