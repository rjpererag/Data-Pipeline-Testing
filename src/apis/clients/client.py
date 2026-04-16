import requests

class Client:

    @staticmethod
    def get(url: str, **kwargs) -> requests.Response:
        headers = kwargs.get("headers", {})
        response = requests.get(
            url=url,
            headers=headers,
        )
        response.raise_for_status()
        return response

    @staticmethod
    def post(url: str, **kwargs) -> requests.Response:
        headers = kwargs.get("headers", {})
        response = requests.post(
            url=url,
            headers=headers,
        )
        response.raise_for_status()
        return response