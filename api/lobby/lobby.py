from pydantic import BaseModel


class JoinLobby(BaseModel):
    id: str = None
    user_id: str = None
