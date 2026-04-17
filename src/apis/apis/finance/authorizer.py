from .db_model.user_db_manager import DBUserManager, User
from dataclasses import dataclass

@dataclass
class Authorization:
    error: str | None = None
    status_code: int | None = None
    status: str | None = None
    is_authorized: bool = False

class Authorizer:

    def __init__(self, db_manager: DBUserManager | None = None):
        self.user_db_manager = db_manager
        self.__is_manager_valid = isinstance(db_manager, DBUserManager)

    def _get_user(self, token: str) -> User | None:
        if not self.__is_manager_valid:
            raise ValueError("Invalid user DB manager")
        return self.user_db_manager.get_user_by_token(token=token)

    def check_auth(self, bearer_token: str) -> Authorization:
        authorization = Authorization()
        try:
            if (not isinstance(bearer_token, str)) or (not bearer_token):
                authorization.error = "Invalid bearer token"
                authorization.status_code = 400
                return authorization

            user = self._get_user(token=bearer_token)

            if user and user.is_active:
                authorization.is_authorized = True
                authorization.status_code = 200
                authorization.status = "ok"

            else:
                authorization.is_authorized = False
                authorization.status_code = 401
                authorization.error = "Unauthorized"

            return authorization

        except Exception as e:
            authorization.error = f"System error: {str(e)}"
            authorization.status_code = 500
            return authorization
