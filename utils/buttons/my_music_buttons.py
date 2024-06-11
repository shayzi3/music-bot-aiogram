
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MusicName(CallbackData, prefix='music_id'):
     music: str
     


async def return_my_music(music_: list[str]) -> InlineKeyboardBuilder:
     build = InlineKeyboardBuilder()
     
     for inline in music_:
          build.button(
               text=inline,
               callback_data=MusicName(music=inline).pack()
          )
          
     build.adjust(3)
     return build.as_markup()