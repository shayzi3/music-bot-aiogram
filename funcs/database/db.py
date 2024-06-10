import json

import aiosqlite

from loguru import logger
from aiosqlite import Connection


class DataBase:
     '''
          Класс содержит функции для работы с базой данных.
          
          db_(  ) -> None
          Создаёт таблицу в базе данных под хранение словаря {название песни: её id}
          
          
          save_musci_id(  ) -> None
          Функция добавляет в словарь новое имя и id
          
          
          check_music_in_db( music_name: str ) -> str | None
          Если музыка, которую ищет пользователь находится в бд,
          то аудио отправляет по file_id из неё.
          
          Вид музыки: {'названиепесни': file_id}
          
          
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
               
               
               
     async def check_music_in_db(self, music_name: str, all_: bool = None) -> list[str] | str | None:          
          async with aiosqlite.connect(self.path_db) as db:
               response = await self._response_sound_(db)
               
               if music_name in response.keys():
                    return response[music_name]
                    
                    
                    
     async def add_new_music_to_user(self, data: list[str], id: int) -> None:
          async with aiosqlite.connect(self.path_db) as db:
               response = await db.execute("SELECT musics FROM userdb WHERE id = ?", [id])
               response = await response.fetchone()
               response: list = json.loads(response[0])
               
               response.append(data)
               
               await db.execute("UPDATE userdb SET musics = ? WHERE id = ?", [json.dumps(response), id])
               await db.commit()
               
               
               
     async def music_at_user(self, id: int) -> list[list[str]] | None:
          async with aiosqlite.connect(self.path_db) as db:
               user = await db.execute("SELECT musics FROM userdb WHERE id = ?", [id])
               user = await user.fetchone()
               user = json.loads(user[0])
               
               if user:
                    return user
               
               
     async def _response_sound_(self, db: Connection) -> dict:
          response = await db.execute("SELECT sounds FROM sound")
          response = await response.fetchone()
          response: dict = json.loads(response[0])
               
          return response
     
               
               
               