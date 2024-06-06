import os
import asyncio
import random

import aiohttp
import requests

from bs4 import BeautifulSoup
from loguru import logger


async def search_soup(url: str) -> BeautifulSoup:     
     async with aiohttp.ClientSession() as session:
          async with session.get(url) as response:
               if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    
                    return soup
     return None



async def get_data(soup: BeautifulSoup) -> list[str]:
     block = soup.find('div', class_='track__info')
     if not block:
          return None

     name = block.find('div', class_='track__title').text
     author = block.find('div', class_='track__desc').text
     time = block.find('div', class_='track__fulltime').text
     link = block.find('a', class_='track__download-btn').get('href')
     
     return [link, name, author, time]



async def download_mp3(data: list[str], id_user: int) -> list[str]:
     name_author = f'{data[1].strip()} - {data[2].strip()}'
     path = await decrease(id_=id_user)
     
     get_ = requests.get(data[0])
     
     with open(path, 'wb') as f:
          f.write(get_.content)
          logger.debug(f'Файл {path} бы сохранён успешно.')
     
     return [name_author, path]



async def finder_sounds(sing: str, id_: int) -> tuple | dict | list[str]:
     link = f'https://rus.hitmotop.com/search?q={sing.strip().lower().replace(" ", "+")}'
     logger.info(f'{id_} начал поиск песни {sing}')
          
     data = await search_soup(url=link)
     if data:
          get = await get_data(data)          
          if get:  
               return await download_mp3(get, id_user=id_)
          
          else:
               # Трека не существует.
               return ()
     else:
          # Технические неполадки у сервиса.
          return {}
     
     
async def delete_path_to_audio(path: str) -> None:
     await asyncio.sleep(60)
     
     if os.path.exists(path):
          os.remove(path)
          logger.debug(f'Файл: {path} был удалён самостоятельно!')
          
          
async def decrease(id_: int) -> str:
     symbols = ['!', '@', '$', '%', '^', '&', '(', ')', '+', '=']
     rnd_symbol = random.choice(symbols)
     
     path = 'audio/' + str(id_) + f'{rnd_symbol}.mp3'
     return path