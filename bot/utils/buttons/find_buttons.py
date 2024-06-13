

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MusicUserAdd(CallbackData, prefix='music_add'):
     music: str
     
class MusicUserDel(CallbackData, prefix='music_del'):
     music: str



async def button_add_song(name_audio: str) -> InlineKeyboardBuilder:
     build = InlineKeyboardBuilder()
     
     build.button(text='Добавить', callback_data=MusicUserAdd(music=name_audio).pack())
     build.button(text='Убрать сообщение.', callback_data=MusicUserAdd(music='del_music'))
     
     return build.as_markup()



async def button_delete_song(name_audio: str) -> InlineKeyboardBuilder:
     build = InlineKeyboardBuilder()
     
     build.button(text='Удалить', callback_data=MusicUserDel(music=name_audio).pack())
     build.button(text='Убрать сообщение.', callback_data=MusicUserDel(music='del_music'))
     
     return build.as_markup()