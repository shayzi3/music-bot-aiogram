

from aiogram.types import CallbackQuery
from aiogram import Router

from bot.utils.buttons import find_buttons as find
from bot.database import db


router = Router()


@router.callback_query(find.MusicUserAdd.filter())
async def music_saver(query: CallbackQuery, callback_data: find.MusicUserAdd) -> None:
     base = db.DataBase()
     
     if callback_data.music == 'del_music':
          await query.message.delete()
          return
     
     
     await base.add_new_music_to_user(
          id=query.from_user.id,
          name_music=callback_data.music
     )
     
     await query.message.edit_reply_markup(
          reply_markup=await find.button_delete_song(name_audio=callback_data.music)
     )
     
     await query.message.answer('Песня сохранена успешно.')
     await query.answer()
     
     
     
@router.callback_query(find.MusicUserDel.filter())
async def music_deleter(query: CallbackQuery, callback_data: find.MusicUserDel) -> None:
     base = db.DataBase()
     
     if callback_data.music == 'del_music':
          await query.message.delete()
          return
     
     await base.delete_music_user(
          id=query.from_user.id,
          name_music=callback_data.music
     )
     
     await query.message.edit_reply_markup(
          reply_markup=await find.button_add_song(name_audio=callback_data.music)
     )
     
     await query.message.answer('Песня успешно удалена.')
     await query.answer()
     
     

     
     
     