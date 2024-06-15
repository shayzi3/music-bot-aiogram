import asyncio
import os

from loguru import logger
from aiogram import Bot, Dispatcher

from bot.handlers.user_commands import start_, find, my_music
from bot.callbacks import find_callback, music_callback
from bot.database import db



async def main() -> None:
     bot = Bot(os.environ.get('TOKEN'))
     dp = Dispatcher()
     base = db.DataBase()
     
     logger.info('Bot ready!')
     
     await base.db_()
     
     dp.include_routers(
          start_.router,
          find.router,
          my_music.router,
          find_callback.router,
          music_callback.router
     )
     
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)
     
     
     
if __name__ == '__main__':
     asyncio.run(main())
     
     