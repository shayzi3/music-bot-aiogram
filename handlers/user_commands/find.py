import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from utils.states.state_find import FindMusic
from scripts.music import finder_sounds, delete_path_to_audio
from utils.buttons import find_buttons as fn



router = Router()


@router.message(Command(commands=['find', 'music', 'fm']))
async def find_music(message: Message, state: FSMContext) -> None:
     await state.set_state(FindMusic.music)
     await message.answer('Введите название песни.')
     
     
     
@router.message(FindMusic.music, F.text)
async def music(message: Message, state: FSMContext) -> None:
     await state.update_data(music=message.text)
     
     response = await finder_sounds(sing=message.text, id_=message.from_user.id)
     
     if isinstance(response, tuple):
          await message.answer('Такой песни не существует!')
          return
          
     elif isinstance(response, dict):
          await message.answer('Тех. неполадки у сервиса!')
          return
     
     await message.answer(
          text=f'Вот, что я нашёл по запросу: {message.text}', 
          reply_markup=await fn.button_title(
               path_to_audio=response[1], 
               title=response[0]
               )
          )
     await state.clear()
     
     await delete_path_to_audio(response[1])
