


class Reduction:
     '''
          Сокращение author_name из find.py до 64 символов в байтовом виде. 
          Для хранения в callback_data inline кнопки.
          
     '''
     
     @staticmethod
     async def reduction(string: str) -> str:
          song = 'music_add:' + string
          
          while len(song.encode()) > 64:
               song = song[:-1]
               
               string = string[:-1]
               
               
                                        
          return string
                    