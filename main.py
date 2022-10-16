from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from const import START_MESSAGE
from RatesAggregator import RatesAggregator

API_TOKEN = config('TELEGRAM_BOT_API_TOKEN', cast=str)

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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)