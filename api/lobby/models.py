from pydantic import BaseModel


class CreateLobby(BaseModel):
    user_id: str = None
    username: str = None

class LobbyBase(BaseModel):
    round_number: int
    lobby_name: str


class InviteRequest(BaseModel):
    lobby_id: str
    lobby_name: str