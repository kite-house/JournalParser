from aiogram import Bot
from os import getenv
from src.commands import dp
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

bot = Bot(token=getenv('TELEGRAM_ACCESS_TOKEN'))

if __name__ == "__main__":
    logging.info('Start System')
    asyncio.run(dp.start_polling(bot))