

from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

from funcs.database import db
from utils.buttons import my_music_buttons as my


router = Router()


@router.message(Command(commands=['my', 'storage']))
async def my_music(message: Message) -> None:
     base = db.DataBase()
     
     user = await base.music_at_user(id=message.from_user.id)
     if user:          
          await message.answer(
               text='Ваша музыка.',
               reply_markup=await my.return_my_music(
                    music_=user
               )
          )
          return
             
     await message.answer(text='У вас нет сохранённой музыки.')