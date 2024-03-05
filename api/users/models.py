from pydantic import BaseModel


class UserCreate(BaseModel):
    id: str = None
    name: str
    password: str
