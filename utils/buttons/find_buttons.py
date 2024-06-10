

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MusicUser(CallbackData, prefix='music'):
     music: str


async def button_add_song(name_audio: str) -> InlineKeyboardBuilder:
     build = InlineKeyboardBuilder()
     
     build.button(text='Добавить ➕', callback_data=MusicUser(music=name_audio).pack())
     return build.as_markup()