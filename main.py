"""
This is a echo bot.
It echoes any incoming text messages.
"""

from aiogram import Bot, Dispatcher, executor, types

from RatesAggregator import RatesAggregator
from RatesTelegramView import create_table_view

API_TOKEN = '5636861019:AAFutqqgirdqcSd-RtnZOwQtYYaNroDxFz0'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['get_rates'])
async def get_rates(message: types.Message):
    aggregator = RatesAggregator()
    rates_string = ''
    for extractor in aggregator.aggregate():
        rates_string += create_table_view(extractor)

    await message.answer(rates_string, disable_web_page_preview = True, parse_mode = 'HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)