from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot
from handlers import start
import config

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

start.reg(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
