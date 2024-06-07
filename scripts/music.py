

from bs4 import BeautifulSoup
from loguru import logger

from scripts import soups

async def get_data(soup: BeautifulSoup) -> list[str]:
     block = soup.find('div', class_='track__info')
     if not block:
          return None

     name = block.find('div', class_='track__title').text
     author = block.find('div', class_='track__desc').text
     link = block.find('a', class_='track__download-btn').get('href')
     
     return [link, name.strip(), author.strip()]



async def return_short_url(data: list[str]) -> str:
     sup = soups.SearchSoups()
     
     short_url = await sup.short_music_soup(tiny=data[0])
     name = data[1] + '-' + data[2]
     
     return [short_url, name]



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