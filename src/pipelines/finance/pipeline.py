import uuid
from src.apis.clients.finance import FinanceAPIClient
from src.apis.clients.dataclasses.prices import Price

class FinancePipeline:

    def __init__(self, token: str, params: dict ,**kwargs):
        self.client = FinanceAPIClient(
            base_url=kwargs.get("base_url", "http://127.0.0.1:5001"),
            token=token,
            endpoints=kwargs.get("endpoints", {})
        )

        self.params=params
        self.symbol = params["symbol"]
        self.threshold = params["threshold"]

    @staticmethod
    def process_price(
            price: Price,
            threshold: float,
    ) -> dict:

        order_id = uuid.uuid4().hex
        if price.price <= threshold:
            return {"order": "sell", "order_id": order_id, "price_data": {**price.model_dump()}}
        return {"order": "buy", "order_id": order_id, "price_data": {**price.model_dump()}}

    @staticmethod
    def execute_order(order: dict) -> None:
        print(f"Executing order {order['order_id']}: {order['order'].upper()}")

    def run(self) -> None:
        try:
            self.client.authenticate()
            price_raw = self.client.get_price(symbol=self.symbol)
            parsed_price = self.client.parse_price(price_raw, self.symbol)
            order = self.process_price(parsed_price, threshold=self.threshold)
            self.execute_order(order=order)
        except Exception as e:
            print(f"Error executing pipeline: {str(e)}")
