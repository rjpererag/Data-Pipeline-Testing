from src.processors.fx_converter import FXConverter
from src.processors.symbol_sanitizer import SymbolSanitizer
from src.apis.apis.finance.app import app
from src.apis.clients.finance import FinanceAPIClient
from src.pipelines.finance.pipeline import FinancePipeline
from src.pipelines.finance.pipeline_executor import run_pipeline


def convert():
	rates = {"EUR": 1.08, "GBP": 1.27, "JPY": 0.0067}
	converter = FXConverter(rates=rates)
	print(converter.convert_to_usd(amount=100.0, currency="USD"))


def sanitize():
	symbols = ["USD", "EUR", "GBP", "JPY"]
	sanitizer = SymbolSanitizer(symbols=symbols)

	print(sanitizer.sanitize(symbol=" usd"))
	print(sanitizer.sanitize(symbol="Eur"))
	print(sanitizer.sanitize(symbol=None))


def finance_api():

	# endpoint = "/auth/status"
	endpoint = "/prices/usdt"

	with app.test_client() as client:

		headers = {"Authorization": "Bearer secret-123"}
		response = client.get(
			endpoint,
			headers=headers,
		)
		print(response.status_code)
		print(response.json)


def finance_client():
	# endpoints = {"authentication": "v2/new/auth/status"}
	client = FinanceAPIClient(
		base_url="http://127.0.0.1:5001",
		token="secret-123",
		# endpoints=endpoints,
	)

	client.authenticate()
	msg = "Authenticated" if client.is_authenticated else "Unauthenticated"
	print(msg)

	symbol = "btc"
	price = client.get_price(symbol=symbol)
	print(price)


def finance_pipeline():
	pipeline = FinancePipeline(
		token="secret-123",
		params={"threshold": 10000}
	)
	pipeline.run()


def finance_pipeline_executor():
	run_pipeline()


if __name__ == "__main__":
	finance_pipeline_executor()

