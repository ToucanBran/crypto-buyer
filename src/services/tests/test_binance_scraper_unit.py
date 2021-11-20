import pytest
from services import BinanceScraper
from .test_data_generators.binance_tdg import articles, announcements
from services.tests.models import MockResponse
from unittest.mock import MagicMock, patch

@patch("services.binance_scraper.CoinService")
@patch("services.binance_scraper.requests.get")
@pytest.mark.parametrize("latest_article_id, expected_total_coins", [(71268, 3), (72774, 1), (72789, 0)])
def test_givenArticles_when_getLatestCoinscalledWithArticleId_expectExpectedNumberOfNewCoins(mock_get_req: MagicMock, mock_coin_service: MagicMock, latest_article_id, expected_total_coins):
    mock_coin_service.exists.return_value = False
    mock_get_req.return_value = MockResponse(announcements, 200)
    binance_scraper = BinanceScraper(mock_coin_service)
    total_coins = len(binance_scraper.get_latest_coins(latest_article_id))
    assert total_coins == expected_total_coins


@patch("services.binance_scraper.CoinService")
@pytest.mark.parametrize("exists, expected_coins", [(True, []), (False, ["BNX", "CHESS", "RGT"])])
def test_givenArticles_when_parseNewCoinscalled_expectExpectedNewCoins(mock_coin_service: MagicMock, exists, expected_coins):
    mock_coin_service.exists.return_value = exists
    binance_scraper = BinanceScraper(mock_coin_service)
    new_coins = binance_scraper.parse_new_coins_from_announcements([article["title"] for article in articles])
    new_coins.sort()
    assert new_coins == expected_coins
    