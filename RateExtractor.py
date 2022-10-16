from abc import ABC, abstractmethod

import requests as requests
from bs4 import BeautifulSoup

from Models import Rate


class BaseRateExtractor(ABC):
    name: str
    source_url: str
    rates: list[Rate]
    _allowed_currencies: tuple = ('USD', 'UAH', 'EUR')


    @abstractmethod
    def extract(self):
        pass


class ObmenkaRateExtractor(BaseRateExtractor):
    name = 'Обменка Сумы'
    source_url = "https://obmenka.sumy.ua/"
    rates = None

    def __init__(self):
        self.rates = []

    def extract(self):
        self.__parseWebPage()

    def __parseWebPage(self):
        page = requests.get(self.source_url)

        soup = BeautifulSoup(page.content, "html.parser")
        table_container = soup.find(id = "mobile")
        table_rows = table_container.find_all("tr")
        # remove placeholder row.
        table_rows.pop(0)

        self.__processRows(table_rows)

    def __processRows(self, rate_rows):
        for row in rate_rows:
            currency_pair, purchase, sale = row.find_all('td')
            main_currency, secondary_currency = currency_pair.text.split('/')
            if (main_currency not in self._allowed_currencies
                    or secondary_currency not in self._allowed_currencies):
                continue

            purchase_price = float(purchase.text)
            sale_price = float(sale.text)
            rate = Rate(main_currency, secondary_currency, purchase_price, sale_price)
            self.rates.append(rate)


class KursRateExtractor(BaseRateExtractor):
    name = 'Курс Сумы'
    source_url = "https://kurs.sumy.ua/"
    rates = None

    def __init__(self):
        self.rates = []

    def extract(self):
        self.__parseWebPage()

    def __parseWebPage(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

        page = requests.get(self.source_url, headers = headers)
        soup = BeautifulSoup(page.content, "html.parser")
        panel_container = soup.find(id = "panel1")
        table_container = panel_container.find('div', class_ = "col-sm-12 board-table")
        rate_rows = table_container.find_all('div', class_ = "row")

        self.__processRows(rate_rows)

    def __processRows(self, rate_rows):
        for row in rate_rows:
            currency_pair = row.find('div', class_ = 'name')
            if currency_pair is None:
                continue

            main_currency, secondary_currency = currency_pair.text.strip().split('/')
            if (main_currency not in self._allowed_currencies
                    or secondary_currency not in self._allowed_currencies):
                continue

            buy_tag = row.find('div', class_ = 'buy')
            buy_tag.find('span').clear()
            purchase_price = float(buy_tag.text.strip())

            sale_tag = row.find('div', class_ = 'sale')
            sale_tag.find('span').clear()
            sale_price = float(sale_tag.text.strip())

            rate = Rate(main_currency, secondary_currency, purchase_price, sale_price)
            self.rates.append(rate)


class Money24RateExtractor(BaseRateExtractor):
    name = 'MONEY 24'
    source_url = "https://money-24.sumy.ua/ru/"
    rates = None

    def __init__(self):
        self.rates = []

    def extract(self):
        self.__parseWebPage()

    def __parseWebPage(self):
        page = requests.get(self.source_url)
        soup = BeautifulSoup(page.content, "html.parser")
        table_container = soup.find(id = "table-roznica")
        table_rows = table_container.find_all('tr')
        # remove placeholder row.
        table_rows.pop(0)
        self.__processRows(table_rows)

    def __processRows(self, rate_rows):
        for row in rate_rows:
            currency_pair_container = row.find('div', class_ = 'currency-name')

            # /usd-uah/ string.
            raw_currency_pair = currency_pair_container.find('a')['href']
            main_currency, secondary_currency = raw_currency_pair[1:-1].split('-')
            main_currency = main_currency.upper()
            secondary_currency = secondary_currency.upper()
            if (main_currency not in self._allowed_currencies
                    or secondary_currency not in self._allowed_currencies):
                continue

            buy_tag = row.find('span', class_ = 'buy')
            purchase_price = float(buy_tag.text.strip())

            sale_tag = row.find('span', class_ = 'pay')
            sale_price = float(sale_tag.text.strip())

            rate = Rate(main_currency, secondary_currency, purchase_price, sale_price)
            self.rates.append(rate)
