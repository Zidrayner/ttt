import os

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv



user = Router()
load_dotenv()

@user.message(CommandStart())
async def start(message: Message):
    await message.answer('Hi')


