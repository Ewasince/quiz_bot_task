import asyncio
import logging
import sys
from logging import handlers

from aiogram import Bot, Dispatcher

from config import config
# from handlers import common_router, find_cve_router, cvss_router, vector_router, complexity_router, valuable_cve_router, \
#     pocs_router
from handlers import common_router



# Создание логера
log = logging.getLogger('')
log.setLevel(logging.DEBUG)
format = logging.Formatter(
    '%(filename)17s[LINE:%(lineno)3d]# %(levelname)-6s [%(asctime)s]  %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(format)
console_handler.setLevel(config.log_level)
log.addHandler(console_handler)

file_handler = handlers.TimedRotatingFileHandler(
    config.log_file,
    when='midnight',
    backupCount=14,
    encoding=None,
    delay=False,
    utc=True)
file_handler.setFormatter(format)
file_handler.setLevel('DEBUG')
log.addHandler(file_handler)


async def main() -> None:
    '''
    Входная точка проекта

    :return:
    '''

    dp = Dispatcher()

    dp.include_routers(
        common_router,
    )

    bot = Bot(config.bot_token, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    log.debug(f'bot starter with config: {config.__dict__}')

    asyncio.run(main())
