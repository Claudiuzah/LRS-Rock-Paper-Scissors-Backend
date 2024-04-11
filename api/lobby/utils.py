from db.models import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from db.models import Lobby



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_lobby_data(id: str, lobby_name=str, db=Depends(get_db)):
    data = db.query(Lobby).filter_by(id=Lobby.id).first().filter_by(lobby_name=Lobby.name).first()
    return data



def create_lobby():
    pass
