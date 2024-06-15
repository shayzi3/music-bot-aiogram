
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(
     keyboard=[
          [
               KeyboardButton(
                    text='/music'
               ),
               KeyboardButton(
                    text='/find'
               )
          ]
     ],
     resize_keyboard=True,
     one_time_keyboard=True
)