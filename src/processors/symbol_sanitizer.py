class SymbolSanitizer:

    def __init__(self, symbols: list[str]):
        self.symbols = symbols

    @staticmethod
    def process_symbol(symbol: str) -> str:
        symbol_stripped = symbol.strip()
        symbol_upper = symbol_stripped.upper()
        return symbol_upper

    def sanitize(self, symbol: str):

        if not isinstance(symbol, str):
            raise TypeError(f"Symbol is not a valid string: {symbol}")

        processed_symbol = self.process_symbol(symbol)

        if processed_symbol not in self.symbols:
            raise ValueError(f"Symbol not found: {symbol}")

        return processed_symbol
