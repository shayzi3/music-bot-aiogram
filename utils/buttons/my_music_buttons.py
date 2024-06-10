
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class MusicID(CallbackData, prefix='music_id'):
     file_id: str


async def button_my_music(music: list[list[str]]) -> InlineKeyboardMarkup:
     inline = []
     
     beetween = []
     for once in range(len(music)):
          if once % 5 != 0 or once == 0:
               beetween.append(
                    InlineKeyboardButton(
                         text=music[once][1], 
                         callback_data=MusicID(file_id=str(music[once][0]))
                    )
               )
          else:
               beetween = []
               
          if beetween not in inline:
               inline.append(beetween)
          
     buttons = InlineKeyboardMarkup(inline_keyboard=inline)
     
     return buttons
     