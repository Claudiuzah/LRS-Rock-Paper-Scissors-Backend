from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from api.lobby.utils import  create_lobby
from api.lobby.models import CreateLobby
from api.lobby.utils import get_db, get_lobby_data
from sqlalchemy.orm import Session
from . import crud, models
from requests import get as requests


db_dependency = Annotated[Session, Depends(get_db)]

lobby_router = APIRouter(
    prefix="/api/lobby",
    tags=["lobby"]
)


@lobby_router.post("/create")
async def create_lobby(lobby_data: CreateLobby):
    lobby = get_lobby_data()
    if lobby is None:
        lobby = create_lobby(lobby_data)

    return lobby


def get_online_users(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            online_users = response.json()
            return online_users
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch online users")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching online users")

# Define the route handler
@lobby_router.get("/online_users")
async def fetch_online_users():
    api_url = "https://example.com/get_online_users"  # Replace with your actual API URL
    online_users = get_online_users(api_url)
    if online_users:
        return online_users
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch online users")


def invite_by_name(lobby_name: str, lobby_id: int, db: Session):
    lobby = crud.get_lobby_by_lobby_name(db, lobby_name)
    if lobby:
        pass
        #TODO: Lobby found, add player to lobby
        #TODO: Implement logic to add player to the lobby
    else:
        raise HTTPException(status_code=404, detail="Invalid invite code")

# >>>>>>> abcb736d6ea56b2d6331f21b6e7d504aa2fcddae


@lobby_router.post("/user/choice")
async def user_choice():
    pass


@lobby_router.put("/player_status")
# >>>>>>> abcb736d6ea56b2d6331f21b6e7d504aa2fcddae
async def player_status():
    pass#online offline



@lobby_router.get("/points")
async def points():
    pass


@lobby_router.get("/{lobby_id}")
async def get_lobby():
    pass

# @refresh-token_router.post("/refresh")

