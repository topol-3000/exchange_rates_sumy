from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from decouple import config

from const import START_MESSAGE
from RatesAggregator import RatesAggregator

API_TOKEN = config('TELEGRAM_BOT_API_TOKEN', cast=str)
WEBHOOK_URL = config('WEBHOOK_URL', cast=str)
WEBAPP_HOST = config('WEBAPP_HOST', cast=str)
WEBAPP_PORT = config('WEBAPP_PORT', cast=int)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(START_MESSAGE)


@dp.message_handler(commands=['get_rates'])
async def get_rates(message: types.Message):
    aggregator = RatesAggregator()
    rates_string = await aggregator.aggregate()
    await message.answer(rates_string, disable_web_page_preview = True, parse_mode = 'HTML')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )