from fastapi import APIRouter
from api.lobby.utils import get_lobby_data, create_lobby
from api.lobby.models import CreateLobby

lobby_router = APIRouter(
    prefix="/api/lobby",
    tags=["lobby"]
)


@lobby_router.post("/create")
async def create_lobby(lobby_data: CreateLobby):
    lobby = get_lobby_data(lobby_data)
    if lobby is None:
        lobby = create_lobby(lobby_data)

    return lobby

@lobby_router.get("/onlineplayers")
async def online_players():
    pass


@lobby_router.put("/invite")
async def invite():
    pass


@lobby_router.post("/user/choice")
async def user_choice():
    pass


@lobby_router.put("/playerstatus")
async def player_status():
    pass


@lobby_router.get("/points")
async def points():
    pass


@lobby_router.get("/{lobby_id}")
async def get_lobby(lobby_id):
    pass


