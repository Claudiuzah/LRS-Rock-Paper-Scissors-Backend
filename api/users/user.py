from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session
from db.models import User, GameSession
from api.users.utils import get_db
from api.users.models import UserProfileStatistics
import uuid

user_router = APIRouter(prefix="/api/user", tags=["user"])


@user_router.get("/{user_id}", response_model=UserProfileStatistics, status_code=status.HTTP_200_OK)
async def get_user_profile_stats(user_id: str = Path(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    total_games = db.query(GameSession).filter_by(user_id=str(user_id)).count()
    total_wins = db.query(GameSession).filter_by(winner_id=str(user_id)).count()
    # total_points = calculate_total_points(user_id, db)

    if total_games > 0:
        win_percentage = (total_wins / total_games) * 100
        loss_percentage = 100 - win_percentage
    else:
        win_percentage = 0
        loss_percentage = 0

    return UserProfileStatistics(
        total_games=total_games,
        total_wins=total_wins,
        # total_points=total_points,
        win_percentage=win_percentage,
        loss_percentage=loss_percentage
    )
