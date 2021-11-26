invalid_base_quotes = [
    ("", ""),
    ("", "BTC"),
    ("USDT", ""),
    (None, None)
]

invalid_place_order = [
    ("", "", 1, "buy", 1),
    ("", "BTC", 1, "buy", 1),
    ("USDT", "", 1, "buy", 1),
    (None, None, 1, "buy", 1),
    ("USDT", "BTC", 1, "", 1),
    ("USDT", "BTC", 1, None, 1),
    ("USDT", "BTC", 1, "buy", 0),
    ("USDT", "BTC", 1, "buy", None),
    ("USDT", "BTC", None, "buy", 1)
]