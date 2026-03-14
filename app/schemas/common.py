from enum import Enum


class Ticker(str, Enum):
    BTC_USD = "btc_usd"
    ETH_USD = "eth_usd"

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(item.value for item in cls)
