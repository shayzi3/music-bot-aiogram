

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class TitleButton(CallbackData, prefix='path'):
     clckru: str
     name: str
     

async def button_title(data: list[str]) -> InlineKeyboardBuilder:
     build = InlineKeyboardBuilder()
     
     separator = data[0].replace(':', '_')
     
     build.button(text=data[1], callback_data=TitleButton(clckru=separator, name=data[1]).pack())
     return build.as_markup()
