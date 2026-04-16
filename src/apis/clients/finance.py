from .client import Client
from .exceptions.authentication import AuthenticationError
from .dataclasses.prices import Price
from pydantic import ValidationError
from dataclasses import dataclass


@dataclass
class FinanceAPIEndpoint:
    authentication: str = "/auth/status"
    price: str = "/prices"

class FinanceAPIClient(Client):

    def __init__(
            self,
            base_url: str,
            token: str,
            **kwargs
    ):
        super().__init__()
        self.base_url = base_url
        self.headers = self._get_headers(token=token)
        self.is_authenticated = False
        self.kwargs = kwargs
        self.endpoints: FinanceAPIEndpoint = self._get_endpoints()

    def _get_endpoints(self) -> FinanceAPIEndpoint:
        if endpoints := self.kwargs.get("endpoints"):
            return FinanceAPIEndpoint(**endpoints)
        return FinanceAPIEndpoint()

    @staticmethod
    def _get_headers(token: str) -> dict | None:
        return {"Authorization": f"Bearer {token}"}

    def _get_full_url(self, endpoint) -> str | None:
        url = f"{self.base_url}{endpoint}"
        return url

    def check_auth(self) -> bool:
        if not self.endpoints.authentication:
            raise TypeError("endpoint must be specified")

        url = self._get_full_url(self.endpoints.authentication)
        response = self.get(url, headers=self.headers)

        if response.status_code == 200:
            return True

        elif response.status_code == 401:
            return False

        return False

    def authenticate(self) -> None:
        self.is_authenticated = self.check_auth()

    @staticmethod
    def parse_price(price: dict, symbol: str) -> Price:
        try:
            return Price(**price)
        except ValidationError as e:
            raise ValueError(f"Data integrity error for {symbol}. {str(e)}")


    def get_price(
            self,
            symbol: str
    ) -> dict:

        if not self.endpoints.price:
            raise TypeError("endpoint must be specified")

        if not self.is_authenticated:
            raise AuthenticationError("Token not valid or need to authenticate")

        url = self._get_full_url(endpoint=f"{self.endpoints.price}/{symbol}")
        response = self.get(url=url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to get price for {symbol}. {response.json().get('error')}")

        return response.json()
