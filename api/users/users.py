from fastapi import APIRouter

from api.users.models import UserCreate
from api.users.utils import get_user_data, create_user

users_router = APIRouter()


@users_router.post("/api/authenticate")
async def authenticate_user(user_data: UserCreate):
    user = get_user_data(user_data)
    if user is None:
        user = create_user(user_data)

    return user
