import json

import aiosqlite

from loguru import logger
from aiosqlite import Connection
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.buttons import find_buttons as find


class DataBase:
     '''
          Класс содержит функции для работы с базой данных.
          
          
          Вид музыки которая передается:  shamanярусский
          
          
          # TODO: db_(  ) -> None
          Создаёт таблицу в базе данных под хранение словаря {название песни: её id}
          Название таблицы: sound
          
          Вид данных:
          sounds: dict[str, list[str]]
          
          sounds - сохраняет полное название трека и id музыки, которую отправляет бот.
               Чтобы в дальнейшем музыку было легче отправлять.
          
          
          
          # TODO: user_db_( id: int ) -> None
          Сохраняет данные пользователя в таблицу.
          Название таблицы: 
          
          Вид данных:
          id: int
          musics: list
          
          id - хранение id
          musics - хранение сохранённой музыки пользователя
          
          
          
          # TODO: save_musci_id( data: dict, name: str ) -> None
          Функция добавляет в базу данных словарь с названием музыки и её file_id
          
          data: dict - {'названиетрека': file_id}
          name: str - название музыки(чтобы проверить существует ли уже такая в бд)
          
          
          
          # TODO: check_music_in_db( music_name: str ) -> str | None
          Если музыка, которую ищет пользователь находится в бд,
          то аудио отправляет по file_id из неё.
          
          music_name: str - название музыки
          
          
          
          # TODO: add_new_music_to_user( id: int, name_music: str ) -> None
          Сохраняет новую музыку пользователю в список
          
          id: int - id пользователя
          name_music: str - название этой музыки, которую добавляю
          
          
          
          # TODO: delete_music_user( id: int, name_music: str ) -> None
          Удаляю музыку у пользователя 
          
          id: int - id пользователя
          name_music: str
          
          
          
          # TODO: music_search_add_del( id: int, music_name: str ) -> InlineKeyboardBuilder
          Проверяем есть music_name у пользователя
          Когда он нажимает на музыку после команды /my или /find, то мы узнаём
          нужно ли 'Добавить' или 'Удалить' эту музыку.
          
          id: int - id пользователя
          music_name: str - название музыки
          
          
          
          # TODO: music_at_user( id: int ) -> list[str] | None
          Возвращаем музыку пользователя
          
          id: int - id пользователя
          
          
          
          # TODO: file_id_about_name( name: str ) -> str
          Возвращаю file_id по названию музыки чтобы отправить в чат.
          Применяется в команде /my
          
          name: str - название музыки
          
          
          
          # TODO: _response_sound_( db: Connection ) -> dict   (staticmethod)
          Возвращаю музыку, которая добавляется в базу данных sound.
          
          
          
          # TODO: _response_music_user_( db: Connection, id: int ) -> list   (statismethod)
          Возвращает музыку пользователя
          
          id: int - id пользователя
          
          
     '''
     
     def __init__(self) -> None:
          self.path_db = 'funcs/data/music.db'
     
     
     
     async def db_(self) -> None:
          async with aiosqlite.connect(self.path_db) as db:
               await db.execute("""CREATE TABLE IF NOT EXISTS sound(
                    sounds TEXT
               )""")
               
               await db.execute("""CREATE TABLE IF NOT EXISTS userdb(
                    id INT,
                    musics TEXT
               )""")
               await db.commit()
               
               await db.execute("INSERT INTO sound VALUES(?)", [json.dumps({})])
               await db.commit()
     
     
     
     async def user_db_(self, id: int) -> None:
          async with aiosqlite.connect(self.path_db) as db:
               response = await db.execute("SELECT musics FROM userdb WHERE id = ?", [id])
               response = await response.fetchone()
               
               if not response:
                    await db.execute("INSERT INTO userdb VALUES(?, ?)", [id, json.dumps([])])
                    await db.commit()
                    
                    logger.debug('New user add to db.')
                    return True
     
     
     
     async def save_music_id(self, data: dict, name: str) -> None:
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_sound_(db)
               
               if name not in response.keys():
                    for item in data.keys():
                         response[item] = data[item]
                    
                    await db.execute("UPDATE sound SET sounds = ?", [json.dumps(response)])
                    await db.commit()
               
               
               
     async def check_music_in_db(self, music_name: str) -> list[str] | str | None:          
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_sound_(db)
               
               if music_name in response.keys():
                    return response[music_name]
                    
                    
                    
     async def add_new_music_to_user(self, id: int, name_music: str) -> None:
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_music_user_(db, id)
               
               if name_music not in response:
                    response.append(name_music)
               
                    await db.execute("UPDATE userdb SET musics = ? WHERE id = ?", [json.dumps(response), id])
                    await db.commit()
               
                              
     
     async def delete_music_user(self, id: int, name_music: str) -> None:
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_music_user_(db, id)
               
               if name_music in response:
                    response.remove(name_music)               
               
                    await db.execute("UPDATE userdb SET musics = ? WHERE id = ?", [json.dumps(response), id])
                    await db.commit()
               
               
               
     async def music_search_add_del(self, id: int, music_name: str) -> InlineKeyboardBuilder:
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_music_user_(db, id)
               
               if music_name in response:
                    return await find.button_delete_song(name_audio=music_name)
               
               return await find.button_add_song(name_audio=music_name)
          
          
          
     async def music_at_user(self, id: int) -> list[str] | None:
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_music_user_(db, id)
               
               if response:
                    return response
          
          
          
     async def file_id_about_name(self, name: str) -> str:
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_sound_(db)
               
               return response[name]
           
           
              
     @staticmethod
     async def _response_sound_(db: Connection) -> dict:
          response = await db.execute("SELECT sounds FROM sound")
          response = await response.fetchone()
          response: dict = json.loads(response[0])
               
          return response
     
     
     
     @staticmethod
     async def _response_music_user_(db: Connection, id: int) -> list:
          response = await db.execute("SELECT musics FROM userdb WHERE id = ?", [id])
          response = await response.fetchone()
          response: list = json.loads(response[0])
          
          return response