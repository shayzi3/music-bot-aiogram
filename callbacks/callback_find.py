import os

from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from utils.buttons.find_buttons import TitleButton


router = Router()


@router.callback_query(TitleButton.filter())
async def audio_send_about_path(query: CallbackQuery, callback_data: TitleButton) -> None:
     if os.path.exists(callback_data.path):
          file = FSInputFile(callback_data.path)
               
          # ! Создать фильтр для сортировки имён чтобы не отправлялось 347627636782).mp3
          
          await query.message.answer_audio(
               audio=file
          )
          os.remove(callback_data.path)
     else:
          await query.message.answer('Повторите поиск песни снова. Файл с ней был удалён.')
     await query.answer()