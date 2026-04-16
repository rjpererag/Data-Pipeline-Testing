from datetime import datetime
import random


def get_base_price(symbol: str) -> float | None:
    symbols_base_price = {
        "btc": 100000,
        "eth": 20000,
    }
    base_price = symbols_base_price.get(symbol)
    return base_price

def get_random_price(symbol: str) -> dict | None:

    base_price = get_base_price(symbol)
    if not base_price:
        return None

    price = round(base_price * random.random(), 2)
    currency = random.choice(["USD", "EUR"])
    return {
        "symbol": symbol,
        "price": price,
        "currency": currency,
        "time": datetime.now().isoformat(),
        "status": "ok",
    }
