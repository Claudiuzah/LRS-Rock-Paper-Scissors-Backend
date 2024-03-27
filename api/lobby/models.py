from pydantic import BaseModel


class CreateLobby(BaseModel):
    id: str = None
    lobby_id: str = None
    user_id: str = None

class LobbyBase(BaseModel):
    round_number: int
    lobby_name: str