from RateExtractor import ObmenkaRateExtractor, KursRateExtractor, Money24RateExtractor


class RatesAggregator:

    def __init__(self):
        self.rate_extractors = [
            ObmenkaRateExtractor(),
            KursRateExtractor(),
            Money24RateExtractor()
        ]

    def aggregate(self):
        for extractor in self.rate_extractors:
            extractor.extract()
            yield extractor
