import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.apis.apis.finance.db_model.user_db_manager import DBUserManager, DBCredentials
from src.apis.apis.finance.db_model.user import Base, User
from src.apis.apis.finance.authorizer import Authorizer
from datetime import datetime, timezone, timedelta


@pytest.fixture(scope="module")
def postgres_db():
    with PostgresContainer("postgres:13") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield postgres


def test_authorizer_with_real_db(postgres_db):
    url = postgres_db.get_connection_url()
    manager = DBUserManager()
    manager.engine = create_engine(url)
    manager.session = sessionmaker(bind=manager.engine)

    with manager.session() as session:
        test_token = "secret-123"
        hashed = manager.get_token_hash(test_token)
        user = User(
            username="ci-test",
            token_hash=hashed,
            is_active=True,
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        )
        session.add(user)
        session.commit()

    auth = Authorizer(db_manager=manager)
    result = auth.check_auth(bearer_token=test_token)

    assert result.is_authorized is True
    assert result.status_code == 200