
from aiogram.types import CallbackQuery
from aiogram import Router

from utils.buttons import my_music_buttons as my_btn
from utils.buttons import find_buttons as fnd
from funcs.database import db


router = Router()


@router.callback_query(my_btn.MusicName.filter())
async def music_profile(query: CallbackQuery, callback_data: my_btn.MusicName) -> None:
     base = db.DataBase()
     
     file_id = await base.file_id_about_name(name=callback_data.music)
     
     await query.message.answer_audio(
          audio=file_id, 
          reply_markup=await base.music_search_add_del(
               id=query.from_user.id, 
               music_name=callback_data.music
          )
     )
     await query.answer()               
               
     
     
