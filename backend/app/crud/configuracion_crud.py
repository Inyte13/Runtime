from backend.app.models.configuracion import DiaDefault
from sqlmodel import Session, select


def read_configuracion(session: Session) -> DiaDefault | None:
  return session.exec(select(DiaDefault)).first()


def save_configuracion(session: Session, config: DiaDefault) -> DiaDefault:
  session.add(config)
  session.commit()
  session.refresh(config)
  return config
