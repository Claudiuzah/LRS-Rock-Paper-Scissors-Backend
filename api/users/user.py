from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from db.models import User, GameSession, Move, User_statistics
from api.users.utils import get_db
from api.users.models import UserProfileStatistics, UpdateUserProfileStats, GameResult, PlayerMove, UserStatsResponse
from dependencies import get_current_user

user_router = APIRouter(prefix="/api/user", tags=["user"])


@user_router.put("/putstats", status_code=status.HTTP_200_OK)
async def put_user_profile_stats(user_data: UpdateUserProfileStats, user_id: str,
                                 db: Session = Depends(get_db),
                                 user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user.total_games_multiplayer = user_data.total_games_multiplayer
    db_user.total_wins_multiplayer = user_data.total_wins_multiplayer
    db_user.total_points_multiplayer = user_data.total_points_multiplayer
    db_user.total_games_singleplayer = user_data.total_games_singleplayer
    db_user.total_wins_singleplayer = user_data.total_wins_singleplayer
    db_user.total_points_singleplayer = user_data.total_points_singleplayer
    db.commit()
    return {"message": "User updated successfully"}


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
    total_games_singleplayer = 0

    if total_games_multiplayer > 0:
        win_percentage_multiplayer = (total_wins_multiplayer / total_games_multiplayer) * 100
        loss_percentage_multiplayer = 100 - win_percentage_multiplayer
    else:
        win_percentage_multiplayer = 0
        loss_percentage_multiplayer = 0

    if total_games_singleplayer > 0:
        win_percentage_singleplayer = (total_wins_singleplayer / total_games_singleplayer) * 100
        loss_percentage_singleplayer = 100 - win_percentage_singleplayer
    else:
        win_percentage_singleplayer = 0
        loss_percentage_singleplayer = 0

    return UserProfileStatistics(
        username=user.username,
        total_games_multiplayer=total_games_multiplayer,
        total_wins_multiplayer=total_wins_multiplayer,
        total_points_multiplayer=0,  # Placeholder
        win_percentage_multiplayer=win_percentage_multiplayer,
        loss_percentage_multiplayer=loss_percentage_multiplayer,
        total_games_singleplayer=total_games_singleplayer,
        total_wins_singleplayer=total_wins_singleplayer,
        total_points_singleplayer=0,  # Placeholder
        win_percentage_singleplayer=win_percentage_singleplayer,
        loss_percentage_singleplayer=loss_percentage_singleplayer
    )


@user_router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    user_stats = db.query(User_statistics).filter(User_statistics.id == user["id"]).first()

    if not user_stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User statistics not found")

    return user_stats


@user_router.post("/singleplayer", status_code=status.HTTP_201_CREATED, response_model=UserStatsResponse)
async def singleplayer_game(game_result: GameResult, db: Session = Depends(get_db),
                            user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    game_session = GameSession(
        lobby_id=game_result.lobby_id,
        winner_id=game_result.winner_id,
        player_ids=game_result.player_ids,
        start_time=game_result.start_time,
        end_time=game_result.end_time
    )
    db.add(game_session)
    db.commit()

    # Store player moves
    for move in game_result.moves:
        player_move = Move(
            session_id=game_session.id,
            player_id=move.player_id,
            choice=move.choice
        )
        db.add(player_move)
    db.commit()

    user_id = user["id"]
    db_user_stats = db.query(User_statistics).filter(User_statistics.id == user_id).first()
    if not db_user_stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User statistics not found")

    db_user_stats.total_games_singleplayer += 1
    if game_result.winner_id == user_id:
        db_user_stats.total_wins_singleplayer += 1
        db_user_stats.total_points_singleplayer += 10  # TODO the points from front

    db.commit()

    return db_user_stats
