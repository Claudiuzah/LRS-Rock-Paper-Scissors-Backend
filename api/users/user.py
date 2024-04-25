from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session
from db.models import User, GameSession, User_statistics
from api.users.utils import get_db
from api.users.models import UserProfileStatistics, UpdateUserProfileStats
from dependencies import get_current_user

# from uuid import UUID

user_router = APIRouter(prefix="/api/user", tags=["user"])


# @user_router.put("/putstats", status_code=status.HTTP_200_OK)
# async def put_user_profile_stats(user_data: UpdateUserProfileStats, user_id: str,
#                                  db: Session = Depends(get_db),
#                                  user: dict = Depends(get_current_user)):
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     db_user.stats.total_games_multiplayer = user_data.total_games_multiplayer
#     db_user.stats.total_wins_multiplayer = user_data.total_wins_multiplayer
#     db_user.stats.total_points_multiplayer = user_data.total_points_multiplayer
#     db_user.stats.total_games_singleplayer = user_data.total_games_singleplayer
#     db_user.stats.total_wins_singleplayer = user_data.total_wins_singleplayer
#     db_user.stats.total_points_singleplayer = user_data.total_points_singleplayer
#     db.commit()
#     return {"message": "User updated successfully"}


@user_router.get("/{user_id}", response_model=UserProfileStatistics, status_code=status.HTTP_200_OK)
async def get_user_profile_stats(user_id: str = Path(...), db: Session = Depends(get_db),
                                 user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    try:
        total_wins_multiplayer = db.query(GameSession).filter_by(winner_id=str(user_id)).count()
        total_wins_singleplayer = db.query(GameSession).filter_by(winner_id=str(user_id)).count()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    total_games_multiplayer = 0
    # game_sesions = db.query(GameSession).all()

    # total_points = calculate_total_points(user_id, db)

    if total_games_multiplayer > 0:
        win_percentage_multiplayer = (total_wins_multiplayer / total_games_multiplayer) * 100
        loss_percentage_multiplayer = 100 - win_percentage_multiplayer
    else:
        win_percentage_multiplayer = 0
        loss_percentage_multiplayer = 0

    total_games_singleplayer = 0

    if total_games_multiplayer > 0:
        win_percentage_singleplayer = (total_wins_singleplayer / total_games_singleplayer) * 100
        loss_percentage_singleplayer = 100 - win_percentage_singleplayer
    else:
        win_percentage_singleplayer = 0
        loss_percentage_singleplayer = 0

    return UserProfileStatistics(
        username=user.username,
        total_games_multiplayer=total_games_multiplayer,
        total_wins_multiplayer=total_wins_multiplayer,
        # total_points_multiplayer=total_points_multiplayer,
        win_percentage_multiplayer=win_percentage_multiplayer,
        loss_percentage_multiplayer=loss_percentage_multiplayer,
        total_games_singleplayer=total_games_singleplayer,
        total_wins_singleplayer=total_wins_singleplayer,
        # total_points_singleplayer=total_points_singleplayer,
        win_percentage_singleplayer=win_percentage_singleplayer,
        loss_percentage_singleplayer=loss_percentage_singleplayer
    )


def get_user(user_id: str, db=Depends(get_db)):
    user = db.query(User_statistics).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
