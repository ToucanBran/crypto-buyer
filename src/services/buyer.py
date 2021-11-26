from gate_api import Order, Ticker
from gate_api.api.spot_api import SpotApi
from services import get_logger, SpotApiWrapper
from models import TradeOptions
from helpers import is_none_or_whitespace
from datetime import datetime

class Buyer:

    def __init__(self, configs, trade_options: TradeOptions, spot_api_wrapper: SpotApiWrapper):
        self._spot_api = None
        self.spot_api_wrapper = spot_api_wrapper
        self.logger = get_logger("buyer")
        self.trade_options = trade_options
        self.configs = configs

    @property
    def spot_api(self) -> SpotApi:
        if self._spot_api is None:
            self._spot_api = self.spot_api_wrapper.spot_api
        return self._spot_api

    async def get_last_price(self, base, quote):
        if is_none_or_whitespace(base) or is_none_or_whitespace(quote):
            raise Exception(
                "Missing base or quote from currency pair to get the last price")
        tickers: list(Ticker) = await self.spot_api.list_tickers(currency_pair=f'{base}_{quote}')
        return tickers[0].last

    async def get_min_amount(self, base, quote):
        if is_none_or_whitespace(base) or is_none_or_whitespace(quote):
            raise Exception(
                "Missing base or quote from currency pair to get the min amount")
        try:
            return await self.spot_api.get_currency_pair(currency_pair=f'{base}_{quote}').min_quote_amount
        except Exception as e:
            self.logger.error(e)

    async def place_order(self, base, quote, amount, side, last_price) -> Order:
        if is_none_or_whitespace(base) or is_none_or_whitespace(quote) or is_none_or_whitespace(side):
            raise Exception("Missing base, quote, or side to place order")
        if last_price == 0:
            raise Exception("Last price cannot be 0 to place an order")
        if amount is None or last_price is None:
            raise Exception("Amount and last price cannot be none")
        try:
            order = Order(amount=str(float(amount)/float(last_price)),
                          price=last_price, side=side, currency_pair=f'{base}_{quote}')
            return await self.spot_api.create_order(order)
        except Exception as e:
            self.logger.error(e)
            raise

    def place_test_order(self, coin, price, trade_options: TradeOptions):
        order_details = f"""
        'symbol': {coin},
        'price': {price},
        'volume': {trade_options.quantity},
        'time': {datetime.timestamp(datetime.now())},
        'tp': {trade_options.trailing_take_profit},
        'sl': {trade_options.stop_loss},
        'id': 'test-order',
        'text': 'test-order',
        'create_time': {datetime.timestamp(datetime.now())},
        'update_time': {datetime.timestamp(datetime.now())},
        'currency_pair': f'{coin}_{trade_options.pairing}',
        'status': 'filled',
        'type': 'limit',
        'account': 'spot',
        'side': 'buy',
        'iceberg': '0'
        """
        self.logger.info('PLACING TEST ORDER')
        self.logger.debug(order_details)

    def store_order(self, order: Order):
        return True
