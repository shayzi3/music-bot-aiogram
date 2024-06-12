import asyncio
import aiohttp
import pyshorteners

from bs4 import BeautifulSoup



class SearchSoups:
     '''     
     search_soup( url: str )  -> BeautifuleSoup | None
          
          Пример url:
          url - https://rus.hitmotop.com/search?q={песня}
          
          Функция возвращает полный html код страницы
          
     
     short_music_soup( tiny: str )  -> str | None
     
          Примеры:
          tiny - https://rus.hitmotop.com/get/music/20240309/APENT_-_Mozhno_ya_s_tobojj_77552797.mp3
          
          Функция вернёт короткую ссылку. Для просто хранения в callback_data
     
     '''
          
     async def search_soup(self, url: str) -> BeautifulSoup | None:  
          async with aiohttp.ClientSession() as session:
               async with session.get(url) as response:
                    if response.status == 200:
                         soup = BeautifulSoup(await response.text(), 'lxml')
                              
                         return soup
          return None



     async def short_music_soup(self, tiny: str) -> str | None:
          short = pyshorteners.Shortener()
          url = short.tinyurl.short(tiny)
          
          return url
               