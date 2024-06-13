import aiohttp

from bs4 import BeautifulSoup



class SearchSoups:
     '''     
     search_soup( url: str )  -> BeautifuleSoup | None
          
          Пример url:
          url - https://rus.hitmotop.com/search?q={песня}
          
          Функция возвращает полный html код страницы
     
     '''
          
     async def search_soup(self, url: str) -> BeautifulSoup | None:  
          async with aiohttp.ClientSession() as session:
               async with session.get(url) as response:
                    if response.status == 200:
                         soup = BeautifulSoup(await response.text(), 'lxml')
                              
                         return soup
          return None