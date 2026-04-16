from .db_model.user_db_manager import DBUserManager, User

class Authorizer:

    def __init__(self):
        self.user_db_manager = DBUserManager()

    def _get_user(self, token: str) -> User:
        return self.user_db_manager.get_user_by_token(token=token)

    def check_auth(self, bearer_token: str) -> bool:
        if isinstance(bearer_token, str):
            user = self._get_user(token=bearer_token)
            return user.is_active
        return False
