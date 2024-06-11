
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.input_file import URLInputFile

from utils.states.state_find import FindMusic
from scripts.music import finder_sounds
from utils.buttons import find_buttons as fnd

from funcs.database import db



router = Router()


@router.message(Command(commands=['find', 'music', 'fm']))
async def find_music(message: Message, state: FSMContext) -> None:
     await state.set_state(FindMusic.music)
     await message.answer('Введите название песни.')
     
     
     
@router.message(FindMusic.music, F.text)
async def music(message: Message, state: FSMContext) -> None:
     await state.update_data(music=message.text)
     
     # ? Ищу песню
     response = await finder_sounds(sing=message.text, id_=message.from_user.id)
     base = db.DataBase()
     
     # ? Формирую название для хранения в базе данных
     author_name = f'{response[2].lower().strip().replace(" ", "")}{response[1].lower().strip().replace(" ", "")}'
     
     if isinstance(response, tuple):
          await message.answer('Такой песни не существует!')
          return
          
     elif isinstance(response, dict):
          await message.answer('Тех. неполадки у сервиса!')
          return
     
     
     # ? Проверяю, есть ли audio в базе данных, если нет, то отправляю через URLInputFile
     file_audio = await base.check_music_in_db(music_name=author_name)
     if not file_audio:
          file_audio = URLInputFile(
               url=response[0],
               timeout=8
          )
          
          
     # ? Проверяю есть ли такая песня у пользователя
     button_add_del = await base.music_search_add_del(
          id=message.from_user.id,
          music_name=author_name
     )
     
     
     # ? Аватар для песни
     file_img = URLInputFile(
          url=response[4],
          timeout=8
     )
     
     
     music = await message.answer_audio(
          audio=file_audio,
          duration=int(response[3].split(':')[0][-1]) * 60,
          performer=response[2],
          title=response[1],
          thumbnail=file_img,
          reply_markup=button_add_del
     )
     await state.clear()
     
     # ? Сохранение в базу данных audio.file_id     
     data = {
          author_name: music.audio.file_id
     }
     await base.save_music_id(data=data, name=author_name)