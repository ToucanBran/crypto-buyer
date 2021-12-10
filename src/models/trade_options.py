from dataclasses import dataclass

@dataclass
class TradeOptions:
    quantity: int = 0
    pairing: str = ""
    test: bool = True
    stop_loss: int = 0
    take_profit: int = 0
    enable_tsl: bool = True
    trailing_stop_loss: int = 0
    trailing_take_profit: int = 0
