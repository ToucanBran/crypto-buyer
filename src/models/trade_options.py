from dataclasses import dataclass

@dataclass
class TradeOptions:
    quantity: int
    pairing: str
    test: bool
    stop_loss: int
    take_profit: int
    enable_tsl: bool
    trailing_stop_loss: int
    trailing_take_profit: int
    
    def import_options(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
