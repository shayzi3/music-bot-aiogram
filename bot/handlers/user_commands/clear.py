
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(Command('clear'))
async def clear_state(message: Message, state: FSMContext) -> None:
     await state.clear()
