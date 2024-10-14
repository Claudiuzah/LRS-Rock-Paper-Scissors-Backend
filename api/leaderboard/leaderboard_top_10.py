from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from db.models import User, User_statistics
from api.users.utils import get_db
from starlette import status

user_stats_router = APIRouter(prefix="/api/user_stats", tags=["user_stats"])


@user_stats_router.get("/username_wins", response_model=list[dict], status_code=status.HTTP_200_OK)
async def get_usernames_and_wins(db: Session = Depends(get_db)):
    try:
        user_wins = (
            db.query(User.username, User_statistics.total_wins_multiplayer)
            .join(User_statistics, User.id == User_statistics.id)
            .order_by(desc(User_statistics.total_wins_multiplayer))
            .limit(10)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    result_list = [
        {"username": user.username, "wins": user.total_wins_multiplayer}
        for user in user_wins
    ]

    return result_list
