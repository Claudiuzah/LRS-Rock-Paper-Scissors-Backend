from . import models
from sqlalchemy.orm import Session
from db.models import Lobby


def get_lobby_by_lobby_name(db: Session, lobby_name: str):
    return db.query(Lobby).filter(lobby_name == lobby_name).first()
