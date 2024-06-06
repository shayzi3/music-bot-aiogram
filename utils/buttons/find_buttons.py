

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class TitleButton(CallbackData, prefix='path'):
     path: str
     name: str
     

async def button_title(path_to_audio: str, title: str) -> InlineKeyboardBuilder:
     build = InlineKeyboardBuilder()
     
     build.button(text=title, callback_data=TitleButton(path=path_to_audio, name=title).pack())
     return build.as_markup()
