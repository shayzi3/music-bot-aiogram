import asyncio
# import os

import aiohttp
import requests
# import telegram_send

from bs4 import BeautifulSoup
from loguru import logger

# async def send_message(txt: list[str]) -> None:
#      await telegram_send.send(audios=[f'{txt[1]}.mp3'])
#      logger.info(f'{txt[0]} отправлен.')
     
#      os.remove(f'{txt[1]}.mp3')


async def search_soup(url: str, song: str) -> BeautifulSoup:
     logger.info(f'Начался поиск песни {song}.')
     
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
     
     logger.info('Песня найдена.')
     return [link, name, author, time]



async def download_mp3(data: list[str]) -> str:
     name_author = f'{data[1].strip()}-{data[2].strip()}'
     
     get_ = requests.get(data[0])
     with open(f'{name_author}.mp3', 'wb') as f:
          f.write(get_.content)
     
     logger.info('Трек скачан.')
     return [f'{name_author} Time: {data[3].strip()}', name_author]


async def main() -> None:
     sing = input('Название песни:')
     link = f'https://rus.hitmotop.com/search?q={sing.strip().lower().replace(" ", "+")}'
     
     data = await search_soup(url=link, song=sing)
     if data:
          get = await get_data(data)
          if get:
               await download_mp3(get)
     
          else:
               logger.info('Трек не найден.')
          
if __name__ == '__main__':
     asyncio.run(main())