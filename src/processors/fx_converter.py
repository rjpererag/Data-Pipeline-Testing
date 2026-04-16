class FXConverter:

    def __init__(self, rates: dict):
        self.rates = rates

    def convert_to_usd(self, amount: float, currency: str) -> float:

        if currency.lower() == "usd":
            return round(amount, 2)

        if currency not in self.rates:
            raise ValueError(f"No exchange rate found for {currency}")

        return round(amount * self.rates[currency], 2)
