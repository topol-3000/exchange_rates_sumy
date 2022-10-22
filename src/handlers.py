from aiogram import types

from const import START_MESSAGE
from RatesAggregator import RatesAggregator


async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(START_MESSAGE)


async def get_rates(message: types.Message):
    """
    This handler will be called when user sends `/get_rates` command
    """
    aggregator = RatesAggregator()
    rates_string = await aggregator.aggregate()
    await message.answer(rates_string, disable_web_page_preview = True, parse_mode = 'HTML')
