
from aiogram import Router
from aiogram.types import CallbackQuery, URLInputFile
from dotenv import load_dotenv

from utils.buttons.find_buttons import TitleButton


router = Router()


@router.callback_query(TitleButton.filter())
async def audio_send_(query: CallbackQuery, callback_data: TitleButton) -> None:
     file = URLInputFile(
          url=callback_data.clckru.replace('_', ':'), 
          filename=callback_data.name
     )
     
     await query.message.answer_audio(audio=file, title=callback_data.name)
     await query.answer()