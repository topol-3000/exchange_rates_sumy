import asyncio

from RateExtractor import KursRateExtractor, Money24RateExtractor, ObmenkaRateExtractor


class RatesAggregator:

    def __init__(self):
        self.__rate_extractors = [
            ObmenkaRateExtractor(),
            KursRateExtractor(),
            Money24RateExtractor()
        ]

    async def aggregate(self):
        await self.__extract_rates()
        return self.__create_view()

    async def __extract_rates(self):
        tasks = [asyncio.create_task(extractor.extract()) for extractor in self.__rate_extractors]
        await asyncio.gather(*tasks)

    def __create_view(self):
        result_string = [extractor.get_table_view() for extractor in self.__rate_extractors]
        return ''.join(result_string)
