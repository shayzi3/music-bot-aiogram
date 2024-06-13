


class Reduction:
     '''
          Сокращение author_name из find.py до 64 символов в байтовом виде. 
          Для хранения в callback_data inline кнопки.
          
     '''
     
     @staticmethod
     async def reduction(string: str) -> str:
          while len(string.encode()) >= 64:
               string = string[:-15]
                                        
          return string
                    