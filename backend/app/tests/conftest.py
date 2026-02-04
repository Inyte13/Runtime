from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from app.core.database import get_session
from app.main import app

# Una bd de mysql para integration y api tests
mysql_engine = create_engine(
  "mysql+pymysql://root:root@localhost:3307/runtime_test", echo=False
)
# Una bd sqlite para unit tests
sqlite_engine = create_engine("sqlite:///:memory:", echo=False)


@pytest.fixture
def session_mysql():
  SQLModel.metadata.create_all(mysql_engine)
  with Session(mysql_engine) as session:
    yield session
  SQLModel.metadata.drop_all(mysql_engine)


@pytest.fixture
def session_sqlite():
  SQLModel.metadata.create_all(sqlite_engine)
  with Session(sqlite_engine) as session:
    yield session
  SQLModel.metadata.drop_all(sqlite_engine)


@pytest.fixture
def client():
  SQLModel.metadata.create_all(mysql_engine)
  def override_get_session():
    with Session(mysql_engine) as session:
      yield session
  app.dependency_overrides[get_session] = override_get_session
  client = TestClient(app)
  yield client
  app.dependency_overrides.clear()
  SQLModel.metadata.drop_all(mysql_engine)
