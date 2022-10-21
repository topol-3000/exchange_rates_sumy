from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook
from decouple import config

from handlers import get_rates, send_welcome

API_TOKEN = config('TELEGRAM_BOT_API_TOKEN', cast=str)
WEBHOOK_URL = config('WEBHOOK_URL', cast=str)
WEBAPP_HOST = config('WEBAPP_HOST', cast=str)
WEBAPP_PORT = config('WEBAPP_PORT', cast=int)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(get_rates, commands=['get_rates'])


async def on_shutdown(dp: Dispatcher):
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()


if __name__ == '__main__':
    # Initialize bot and dispatcher
    bot = Bot(token = API_TOKEN)
    dp = Dispatcher(bot)
    start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
