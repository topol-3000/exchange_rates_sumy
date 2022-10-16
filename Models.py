class Rate:
    # Currency that is bought or sold.
    main_currency: str = None
    # Currency related to which the calculation is made.
    secondary_currency: str = None
    # The price at which the currency is bought.
    purchase: float = None
    # The price at which the currency is sold.
    sale: float = None

    def __init__(self, main_currency, secondary_currency, purchase, sale):
        self.main_currency = main_currency
        self.secondary_currency = secondary_currency
        self.purchase = purchase
        self.sale = sale

    def __str__(self):
        return (f'{self.main_currency}/{self.secondary_currency} -> '
                f'purchase:{self.purchase}; sale:{self.sale}')