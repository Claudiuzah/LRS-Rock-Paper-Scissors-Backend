from fastapi import APIRouter
from api.lobby.utils import get_lobby_data, create_lobby
from api.lobby.models import CreateLobby

lobby_router = APIRouter()


@lobby_router.post("/api/lobby/create")
async def create_lobby(lobby_data: CreateLobby):
    lobby = get_lobby_data(lobby_data)
    if lobby is None:
        lobby = create_lobby(lobby_data)

    return lobby
