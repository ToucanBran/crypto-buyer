# Listen for updates
# receive update check if previously held
# check if coin is supported on exchange
# place order if not
# store order

import os, sys, asyncio
from load_config import load_config
from services import setup_logger, get_logger, RabbitMqWrapper, queue, CoinService, Buyer, SpotApiWrapper
from models.trade_options import TradeOptions

config_path = f"{os.path.dirname(os.path.abspath(__file__))}/config.yml"
    
def handle_new_coin(ch, method, properties, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logger = get_logger("buyer")
    coin = message.decode()
    order = order_coin(coin, CoinService())
    logger.info(f"{coin} will be ordered: {order}")
    if order:
        configs = load_config(config_path)
        spot_api = SpotApiWrapper(configs["exchange"])
        trade_options = TradeOptions(**configs["trade_options"])
        buyer = Buyer(configs, trade_options, spot_api)

        price = loop.run_until_complete(buyer.get_last_price(coin, trade_options.pairing))
        if trade_options.test:
            buyer.place_test_order(coin, price, trade_options)
        else:
            order = loop.run_until_complete(buyer.place_order(coin, trade_options.pairing, trade_options.quantity,'buy', price))
            buyer.store_order(order)
        
    logger.info("Listening for new coins")

def order_coin(coin, coin_service: CoinService):
    return coin_service.is_supported(coin) and not coin_service.previously_held(coin)

def main(configurations):
    logger = get_logger("buyer")    
    with queue(configurations["queue"]) as q:
        logger.info("Listening for new coins")
        q.start_consuming(handle_new_coin)

if __name__ == '__main__':
    logger = setup_logger()
    configs = load_config(config_path)
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