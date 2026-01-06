from sqlmodel import Session

from app.crud.configuracion_crud import read_configuracion, save_configuracion
from app.models.configuracion import DiaDefault
from app.schemas.configuracion_schema import DiaDefaultUpdate


def buscar_configuracion(session: Session) -> DiaDefault:
  config = read_configuracion(session)
  # Si no hay config, uso la default
  if not config:
    config = DiaDefault()
    return save_configuracion(session, config)
  return config


def actualizar_configuracion(session: Session, cambios: DiaDefaultUpdate) -> DiaDefault:
  config = buscar_configuracion(session)
  values = cambios.model_dump(exclude_unset=True)
  config.sqlmodel_update(values)
  return save_configuracion(session, config)
