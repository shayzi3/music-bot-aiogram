

from bs4 import BeautifulSoup
from loguru import logger

from scripts import soups

async def get_data(soup: BeautifulSoup) -> list[str]:
     block = soup.find('div', class_='track__info')
     
     
     if not block:
          return None
     
     img = soup.find('div', class_='track__img').get('style').split("'")[1]
     
     name = block.find('div', class_='track__title').text
     author = block.find('div', class_='track__desc').text
     time = block.find('div', class_='track__fulltime').text
     link = block.find('a', class_='track__download-btn').get('href')
     
     return [link, name.strip(), author.strip(), time, img]



async def return_short_url(data: list[str]) -> str:
     sup = soups.SearchSoups()
     
     short_url = await sup.short_music_soup(tiny=data[0])
     
     # data[1] - название; data[2] - автор; data[3] - время; data[4] - url для заставки аудио
     
     return [short_url, data[1], data[2], data[3], data[4]]



async def finder_sounds(sing: str, id_: int) -> tuple | dict | list[str]:
     logger.info(f'{id_} начал поиск песни {sing}')
     
     sup = soups.SearchSoups()

     link = f'https://rus.hitmotop.com/search?q={sing.strip().lower().replace(" ", "+")}'
     data = await sup.search_soup(url=link)
     
     if data:
          get = await get_data(data)          
          if get:  
               return await return_short_url(data=get)
          
          else:
               # ? Трека не существует.
               return ()
     else:
          # ? Технические неполадки у сервиса.
          return {}