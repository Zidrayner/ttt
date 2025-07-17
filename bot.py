import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from dotenv import load_dotenv

from handlers.user_handlers import user
from handlers.fsm_handlers import fsm_router

async def main():
    print('Бот запущен!')
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv('API'))
    dp = Dispatcher(maintenance_mode=False, fsm_strategy=FSMStrategy.CHAT)
    dp.include_routers(user,fsm_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())