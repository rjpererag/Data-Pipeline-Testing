_FAKE_VALID_TOKENS = {
    "valid_bearer1234": True,
    "not_valid_bearer567": False,
    "parameta-secret-123": True,
    "secret-123": True,
}

class Authorizer:

    def __init__(self):
        self.valid_tokens = self.__get_valid_tokens()

    @staticmethod
    def __get_valid_tokens() -> dict:
        return _FAKE_VALID_TOKENS

    def lookup_token(self, token: str) -> bool:
        if token not in self.valid_tokens:
            return False
        status = self.valid_tokens.get(token, False)
        return status


    def check_auth(self, bearer_token: str) -> bool:
        if isinstance(bearer_token, str):
            return self.lookup_token(bearer_token)
        return False
