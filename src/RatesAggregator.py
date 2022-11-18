import asyncio

import aiohttp
from decouple import config

from RateExtractor import KursRateExtractor, Money24RateExtractor, ObmenkaRateExtractor


EXTRACTING_TIMEOUT = config('EXTRACTING_TIMEOUT', cast=float)


class RatesAggregator:

    def __init__(self):
        self.__rate_extractors = [
            ObmenkaRateExtractor(),
            KursRateExtractor(),
            Money24RateExtractor()
        ]

    async def aggregate(self):
        async with aiohttp.ClientSession() as session:
            coroutines = [extractor.extract(session) for extractor in self.__rate_extractors]
            done, pending = await asyncio.wait(coroutines, timeout = EXTRACTING_TIMEOUT)

            for task in pending:
                task.cancel()

            if not done:
                return 'Ни один сервис не ответил. Попробуйте запросить информацию немного позже.'

        return self.__create_view()

    def __create_view(self):
        result_string = [extractor.get_table_view() for extractor in self.__rate_extractors]
        return ''.join(result_string)
