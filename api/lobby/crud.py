from . import models
from sqlalchemy.orm import Session


def get_lobby_by_invite_code(db: Session, invite_code: str):
    return db.query(models.Lobby).filter(models.Lobby.invite_code == invite_code).first()
