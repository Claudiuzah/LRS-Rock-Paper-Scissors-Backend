from db.models import SessionLocal
from fastapi import Depends
from typing import Annotated
from db.models import Lobby
from sqlalchemy.orm import Session
from api.lobby.models import CreateLobby


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def get_lobby_data(lobby_data,Session):
    data = Session.query(Lobby).filter(Lobby.lobby_name == lobby_data.lobby_name).first()
    return data


def create_lobby(db: db_dependency, lobby_data):
    create_lobby_model = Lobby(
        lobby_name=lobby_data.lobby_name)

    db.add(create_lobby_model)
    db.commit()
    return {"message": "Lobby created successfully"}
