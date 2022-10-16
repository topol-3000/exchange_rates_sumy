from RateExtractor import BaseRateExtractor
from prettytable import PrettyTable


def create_table_view(extractor: BaseRateExtractor):
    result_string = f'{extractor.name}\n{extractor.source_url}\n'
    result_string += '<pre>'
    tb = PrettyTable(padding_width = 0)
    # Add headers
    tb.field_names = [" ", "Покупка", "Продажа"]

    for rate in extractor.rates:
        # Add rows
        tb.add_row([f'{rate.main_currency}/{rate.secondary_currency}',
                    str(rate.purchase), str(rate.sale)])

    result_string += tb.get_string()
    result_string += '</pre>\n'
    return result_string