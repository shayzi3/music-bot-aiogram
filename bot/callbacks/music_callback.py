
from aiogram.types import CallbackQuery
from aiogram import Router

from bot.utils.buttons import my_music_buttons as my
from bot.database import db


router = Router()


@router.callback_query(my.MusicName.filter())
async def music_profile(query: CallbackQuery, callback_data: my.MusicName) -> None:
     base = db.DataBase()
     
     file_id = await base.file_id_about_name(name=callback_data.music)
     
     await query.message.answer_audio(
          audio=file_id[0], 
          reply_markup=await base.music_search_add_del(
               id=query.from_user.id, 
               music_name=callback_data.music
          )
     )
     await query.answer()        
     
     
     
@router.callback_query(my.RightLeft.filter())
async def left_right(query: CallbackQuery, callback_data: my.RightLeft) -> None:
     page = int(callback_data.page)
     len_data = int(callback_data.len_data)
     
     base = db.DataBase()
     
     if callback_data.action == 'left':
         page = page - 1 if page != 0 else len_data - 1
               
               
     elif callback_data.action == 'right':
         page = page + 1 if page != len_data - 1 else 0
               
     
     user = await base.music_at_user(id=query.from_user.id)
     await query.message.edit_reply_markup(
          reply_markup=await my.return_pages_my_music(
               page=page,
               data=user
          )
     ) 
     
     await query.answer()
               
     
     
