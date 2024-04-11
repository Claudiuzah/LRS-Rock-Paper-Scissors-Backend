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

#nu cred ca mai am nevoie de acest fisier