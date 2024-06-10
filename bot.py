import asyncio
import os

from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher

from handlers.user_commands import start_, find, my_music
from funcs.database import db

load_dotenv()

async def main() -> None:
     bot = Bot(os.getenv('TOKEN'))
     dp = Dispatcher()
     base = db.DataBase()
     
     logger.info('Bot ready!')
     
     await base.db_()
     dp.include_routers(
          start_.router,
          find.router,
          my_music.router
     )
     
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)
     
     
if __name__ == '__main__':
     asyncio.run(main())
     
     