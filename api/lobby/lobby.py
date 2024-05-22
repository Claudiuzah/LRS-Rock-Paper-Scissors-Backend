from fastapi import APIRouter, HTTPException, Depends, status
from api.lobby.models import CreateLobby
from api.lobby.utils import db_dependency
from dependencies import get_current_user
from sqlalchemy.orm import Session
from api.lobby.crud import *
from requests import get
from db.models import Lobby
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

lobby_router = APIRouter(
    prefix="/api/lobby",
    tags=["lobby"]
)


@lobby_router.post("/create")
def create_lobby(db: db_dependency, lobby_data: CreateLobby, user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    existing_lobby = db.query(Lobby).filter(Lobby.lobby_name == lobby_data.lobby_name).first()
    if existing_lobby:
        raise HTTPException(status_code=401, detail="Lobby already exists")
    create_lobby_model = Lobby(lobby_name=lobby_data.lobby_name, rounds=lobby_data.rounds, user_id=lobby_data.user_id)

    db.add(create_lobby_model)
    db.commit()
    return {"message": "Lobby created successfully"}


@lobby_router.post("/user/choice")
async def user_choice(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    pass


@lobby_router.put("/player_status")
async def player_status(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    pass  # online offline


@lobby_router.get("/points")
async def points(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    pass


@lobby_router.post("/invite_to_lobby/{lobby_name}")  # Not working
async def invite_to_lobby(lobby_name: str, user_to_invite: str, db: db_dependency,
                          user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    lobby_memberships = db.query(Lobby).filter(Lobby.lobby_name).first()
    if lobby_name not in lobby_memberships:
        raise HTTPException(status_code=404, detail="Lobby not found")

    lobby_memberships[lobby_name].append(user_to_invite)
    return {"message": f"User '{user_to_invite}' invited to lobby '{lobby_name}'"}


@lobby_router.get("/{lobby_id}")
async def get_lobby_by_id(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    pass
