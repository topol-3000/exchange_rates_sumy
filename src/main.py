import asyncio

from aiogram import Bot, Dispatcher, types
from decouple import config

from handlers import get_rates, send_welcome

API_TOKEN = config('TELEGRAM_BOT_API_TOKEN', cast=str)
WEBHOOK_URL = config('WEBHOOK_URL', cast=str)
WEBAPP_HOST = config('WEBAPP_HOST', cast=str)
WEBAPP_PORT = config('WEBAPP_PORT', cast=int)


async def process_event(event, dp: Dispatcher):
    """Converting an AWS Lambda event to an update and handling that update."""
    Bot.set_current(dp.bot)
    update = types.Update.to_object(event)
    await dp.process_update(update)


async def register_handlers(dp: Dispatcher):
    """Registration all handlers before processing update."""
    dp.register_message_handler(send_welcome, commands = ['start', 'help'])
    dp.register_message_handler(get_rates, commands = ['get_rates'])


async def main(event):
    """Asynchronous wrapper for initializing the bot and dispatcher,
    and launching subsequent functions."""

    bot = Bot(token = API_TOKEN)
    dp = Dispatcher(bot)

    await register_handlers(dp)
    await process_event(event, dp)

    return 'ok'


def lambda_handler(event, context):
    """AWS Lambda handler."""
    return asyncio.get_event_loop().run_until_complete(main(event))
