import hashlib
from dataclasses import dataclass
from decouple import config
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .user import User


@dataclass(frozen=True)
class DBCredentials:
    user: str = config("POSTGRES_USER_USER")
    password: str = config("POSTGRES_USER_PASSWORD")
    host: str = config("POSTGRES_USER_HOST")
    port: int = config("POSTGRES_USER_PORT")
    db: str = config("POSTGRES_USER_DB")


class DBUserManager:
    def __init__(self, creds: DBCredentials = DBCredentials()):
        self.db_url = self._get_db_url(creds=creds)
        self.engine = create_engine(self.db_url, echo=False)
        self.session = sessionmaker(bind=self.engine)

    @staticmethod
    def _get_db_url(creds: DBCredentials) -> str:
        return f"postgresql://{creds.user}:{creds.password}@{creds.host}:{creds.port}/{creds.db}"

    def get_user_by_user_name(self, user_name: str) -> User:
        with self.session() as session:
            stmt =  select(User).where(User.username == user_name)
            result = session.execute(stmt).scalar_one_or_none()
            return result

    @staticmethod
    def get_token_hash(token: str) -> str:
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return token_hash

    def get_user_by_token(self, token: str) -> User:
        token_hash = self.get_token_hash(token)
        with self.session() as session:
            stmt =  select(User).where(User.token_hash==token_hash)
            result = session.execute(stmt).scalar_one_or_none()
            return result