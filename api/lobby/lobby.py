from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from api.lobby.utils import  create_lobby
from api.lobby.models import CreateLobby
from api.lobby.utils import get_db, get_lobby_data
from sqlalchemy.orm import Session
from . import crud, models

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


# def get_user(user_id: str, db = Depends(get_db)):
#     user = db.query(User).filter_by(id=user_id).first() reference pt get lobby

@lobby_router.get("/online_players")
async def online_players():
    pass


@lobby_router.post("/invite")
def invite_to_lobby(invite_request: models.InviteRequest, db: Session = Depends(get_db)):
    if invite_request.invite_code:
        invite_by_code(invite_request.invite_code, invite_request.lobby_id, db)
    else:
        raise HTTPException(status_code=400, detail="Invalid invite request")


def invite_by_code(invite_code: str, lobby_id: int, db: Session):
    # Implement logic to handle invitation by code
    lobby = crud.get_lobby_by_invite_code(db, invite_code)
    if lobby:
        pass
        #TODO: Lobby found, add player to lobby
        #TODO: Implement logic to add player to the lobby
    else:
        raise HTTPException(status_code=404, detail="Invalid invite code")


@lobby_router.post("/user/choice")
async def user_choice():
    pass


@lobby_router.put("/player_status")
async def player_status():
    pass


@lobby_router.get("/points")
async def points():
    pass


@lobby_router.get("/{lobby_id}")
async def get_lobby():
    pass

# @refresh-token_router.post("/refresh")
