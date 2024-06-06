
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from scripts import music as ms


router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
     text = f'''
     Приветсвую тебя, <b>{message.from_user.full_name}</b>. Я помогу тебе найти музыку. И сохранить её! 🎵
     '''
     
     await message.answer(text, parse_mode=ParseMode.HTML)