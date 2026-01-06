from sqlmodel import Session, select

from app.models.configuracion import DiaDefault


def read_configuracion(session: Session) -> DiaDefault | None:
  return session.exec(select(DiaDefault)).first()


def save_configuracion(session: Session, config: DiaDefault) -> DiaDefault:
  session.add(config)
  session.commit()
  session.refresh(config)
  return config
