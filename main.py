import os
import asyncio

from typing import Any

from dotenv import load_dotenv

from pyrogram import Client
from pyrogram.client import Client as Client_
from pyrogram.types.messages_and_media import Message
from pyrogram.handlers import MessageHandler


load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

async def function(client: Client_, message: Message) -> None: 
     print(message.text)    
     await message.forward('me')
  
   
app = Client('my_account', api_id, api_hash)

my_handler = MessageHandler(function)
app.add_handler(my_handler)

app.run()
     
     