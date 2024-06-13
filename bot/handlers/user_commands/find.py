import requests

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.input_file import BufferedInputFile

from bot.utils.states.state_find import FindMusic
from scripts.music import finder_sounds
from scripts.reduction import Reduction
from bot.database import db



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
     
     if isinstance(response, tuple):
          await message.answer('Песня не найдена.')
          return
          
     elif isinstance(response, dict):
          await message.answer('Тех. неполадки у сервиса!')
          return
     
     
     # ? Формирую название для хранения в базе данных sound(author_name) и userdb(track)
     author_name = f'{response[2].lower().replace(" ", "")}{response[1].lower().replace(" ", "")}'
     track = f'{response[2]} - {response[1]}'
     
     
     # ? Проверяю длину названия чтобы оно умещалось в callback_data
     author_name = await Reduction().reduction(string=author_name)
     
     
     # ? Проверяю, есть ли audio в базе данных, если нет, то отправляю через URLInputFile
     file_audio = await base.check_music_in_db(music_name=author_name)
     if not file_audio:
          file_audio = BufferedInputFile(
               file=requests.get(response[0]).content,
               filename='name'
          )
          
     # ? Аватар для песни
     file_img = BufferedInputFile(
          file=requests.get(response[4]).content,
          filename='name'
     )     
     
     
     # ? Проверяю есть ли такая песня у пользователя чтобы добавить кнопки 'Добавить', 'Удалить'
     button_add_del = await base.music_search_add_del(
          id=message.from_user.id,
          music_name=author_name
     )
     
     
     # ? Высчитываю время в минутах и секундах. Пример данных: 03:56  или 05:08
     seconds = response[3].split(':')[1]
     if seconds[0] == '0':
          seconds = seconds[1]
     
     
     minutes = response[3].split(':')[0]
     if minutes[0] == '0':
          minutes = minutes[1]
     
     time = (int(minutes) * 60) + int(seconds)
     
     
     # ? Отправляю аудио
     music = await message.answer_audio(
          audio=file_audio,
          duration=time,
          performer=response[2],
          title=response[1],
          thumbnail=file_img,
          reply_markup=button_add_del
     )
     await state.clear()
     
     
     # ? Сохранение в базу данных audio.file_id     
     data = {author_name: [music.audio.file_id, track]}
     await base.save_music_id(data=data, name=author_name)