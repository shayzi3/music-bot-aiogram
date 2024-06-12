
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
     
     
     
@router.callback_query(my_btn.RightLeft.filter())
async def left_right(query: CallbackQuery, callback_data: my_btn.RightLeft) -> None:
     page = int(callback_data.page)
     len_data = int(callback_data.len_data)
     
     base = db.DataBase()
     
     if callback_data.action == 'left':
          if page != 0: page -= 1
               
          else: page = len_data - 1      
               
               
     elif callback_data.action == 'right':
          if page != len_data - 1: page += 1
          
          else: page = 0
               
     
     user = await base.music_at_user(id=query.from_user.id)
     await query.message.edit_reply_markup(
          reply_markup=await my_btn.return_pages_my_music(
               page=page,
               data=user
          )
     ) 
     
     await query.answer()
               
     
     
