
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database import db


class MusicName(CallbackData, prefix='music_id'):
     music: str
     
     
class RightLeft(CallbackData, prefix='pages'):
     action: str
     len_data: int
     page: int


async def return_sorted_my_music(music_: list[str]) -> list[list[str]]:
     '''
     Пример работы фкнкции:
     
     Создаю из списка [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
     список [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11]]
     '''
     
     num = int(str(len(music_) / 5)[-1])
     if num >= 2: 
          once = ((len(music_)) // 5) + 1
          
     else: 
          once = len(music_) // 5
          
     l = 0
     r = 5
     inline: list[list[str]] = []
     
     for _ in range(once):
          inline.append(music_[l:r])
          
          l += 5
          r += 5
     return inline



async def return_pages_my_music(page: int, data: list[str]) -> InlineKeyboardMarkup:
     data = await return_sorted_my_music(music_=data)
     base = db.DataBase()
     
     streight = None
     if len(data) > 1:
          streight = [
               InlineKeyboardButton(
                    text='←',
                    callback_data=RightLeft(action='left', len_data=len(data), page=page).pack()
               ),
               InlineKeyboardButton(
                    text=f'{page + 1} из {len(data)}',
                    callback_data=RightLeft(action='pg', len_data=len(data), page=page).pack()
               ),
               InlineKeyboardButton(
                    text='→',
                    callback_data=RightLeft(action='right', len_data=len(data), page=page).pack()
               )
          ]
     
     
     inline_buttons = []  
     for item in data[page]:
          file_id = await base.file_id_about_name(name=item)
          
          inline_buttons.append(
               [
                    InlineKeyboardButton(
                         text=file_id[1],
                         callback_data=MusicName(music=item).pack()
                    )
               ]
          )
     if streight: 
          inline_buttons.append(streight)
     
      
     buttons = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
     return buttons
          
     
     
     
          
     
          
     
     
     
     