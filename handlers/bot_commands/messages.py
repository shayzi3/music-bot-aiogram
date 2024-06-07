import os

from dotenv import load_dotenv
from aiogram.types import Message
from aiogram import Router, Bot


router = Router()
load_dotenv()

@router.message()
async def echo(message: Message) -> None:
     ...     