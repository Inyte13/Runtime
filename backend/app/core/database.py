from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/runtime_db"
# echo, para ver las lineas sql
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
  SQLModel.metadata.create_all(engine)  # Crear nuestra tablas


def get_session():
  with Session(engine) as session:  # Generando una nueva session para cada conexión
    yield session


SessionDep = Annotated[Session, Depends(get_session)]
