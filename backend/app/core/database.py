from datetime import date
from typing import Annotated

from fastapi import Depends, Path, Query
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = 'sqlite:///./runtime.db'
# echo, para ver las lineas sql
engine = create_engine(
  DATABASE_URL, connect_args={'check_same_thread': False}, echo=False
)


def create_db_and_tables():
  SQLModel.metadata.create_all(engine)  # Crear nuestra tablas


def get_session():
  with Session(
    engine
  ) as session:  # Generando una nueva session para cada conexión
    yield session


SessionDep = Annotated[Session, Depends(get_session)]

