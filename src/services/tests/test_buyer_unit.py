import asyncio, pytest
from services import Buyer
from services.tests.test_data_generators import invalid_base_quotes, invalid_place_order

@pytest.mark.asyncio
@pytest.mark.parametrize("base, quote", invalid_base_quotes)
async def test_given_invalidArgs_when_getLastPriceCalled_then_expectException(base, quote):
    buyer = Buyer(None, None, None)
    with pytest.raises(Exception):
        await buyer.get_last_price(base, quote)

@pytest.mark.asyncio
@pytest.mark.parametrize("base, quote", invalid_base_quotes)
async def test_given_invalidArgs_when_getMinAmountCalled_then_expectException(base, quote):
    buyer = Buyer(None, None, None)
    with pytest.raises(Exception):
        await buyer.get_min_amount(base, quote)

@pytest.mark.asyncio
@pytest.mark.parametrize("base, quote, amount, side, last_price", invalid_place_order)
async def test_given_invalidArgs_when_placeOrderCalled_then_expectException(base, quote, amount, side, last_price):
    buyer = Buyer(None, None, None)
    with pytest.raises(Exception):
        await buyer.place_order(base, quote, amount, side, last_price)
