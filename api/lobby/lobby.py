from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from api.lobby.models import CreateLobby
from api.lobby.utils import db_dependency
from dependencies import get_current_user
from sqlalchemy.orm import Session
from api.lobby.crud import *
from requests import get as requests
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


def get_online_users(api_url, user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            online_users = response.json()
            return online_users
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch online users")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching online users")


@lobby_router.get("/online_users")
async def fetch_online_users(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    api_url = f"https://{HOST}:{PORT}/"
    online_users = get_online_users(api_url)
    if online_users:
        return online_users
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch online users")


def invite_by_name(lobby_name: str, lobby_id: int, db: Session):
    lobby = get_lobby_by_lobby_name(db, lobby_name)
    if lobby:
        pass
        # TODO: Lobby found, add player to lobby
        # TODO: Implement logic to add player to the lobby
    else:
        raise HTTPException(status_code=404, detail="Invalid invite code")


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


@lobby_router.get("/{lobby_id}")
async def get_lobby(user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    pass
