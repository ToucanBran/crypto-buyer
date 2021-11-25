# Listen for updates
# receive update check if previously held
# check if coin is supported on exchange
# place order if not
# store order

import sys
from load_config import load_config
from services import setup_logger, get_logger, RabbitMqWrapper, queue, CoinService
from models.trade_options import TradeOptions
from services import Buyer, SpotApiWrapper
    
async def handle_new_coin(ch, method, properties, coin):
    logger = get_logger("buyer")
    order = order_coin(coin, CoinService())
    logger.info(f"{coin} will be ordered: {order}")
    if not order:
        return

    configs = load_config("config.yml")
    spot_api = SpotApiWrapper(configs["exchange"])
    trade_options = TradeOptions()
    trade_options.import_options(configs["trade_options"])
    buyer = Buyer(configs, trade_options, spot_api)
    price = await buyer.get_last_price(coin, trade_options.pairing)
    if trade_options.test:
        buyer.place_test_order(coin, price, trade_options)
    else:
        order = await buyer.place_order(coin, trade_options.pairing, trade_options.quantity,'buy', price)
        buyer.store_order(order)
        
    return True

def order_coin(coin, coin_service: CoinService):
    return coin_service.is_supported(coin) and not coin_service.previously_held(coin)

def main(configurations):
    logger = get_logger("buyer")    
    with queue(configurations["queue"]) as q:
        logger.info("Listening for new coins")
        q.start_consuming(handle_new_coin)

if __name__ == '__main__':
    logger = setup_logger()
    configs = load_config("config.yml")
    rmq = RabbitMqWrapper(configs["queue"])
    channel = None
    try_count = 0
    while try_count < 3 and channel is None:
        try:
            channel = rmq.open_channel()
        except Exception as e:
            logger.debug(e)
            logger.info(f"Try {try_count + 1}: Unable to connect to the new coin queue")
            try_count = try_count + 1

    if not rmq.channel_connected():
        logger.info("Unable to connect to connect to the queue")
        sys.exit(1)

    rmq.close_connection()

    main(configs)