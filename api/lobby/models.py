from pydantic import BaseModel


class CreateLobby(BaseModel):
    lobby_name: str
    user_id: str
    rounds: int = 1


class LobbyBase(BaseModel):
    round_number: int
    lobby_name: str


class InviteRequest(BaseModel):
    lobby_id: str
    lobby_name: str
