# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from starlette import status
# from db.models import User
# from api.users.utils import get_db
# from api.leaderboard.models import LeaderboardResponse
#
# leaderboard_router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])
#
#
# @leaderboard_router.get("/", response_model=LeaderboardResponse, status_code=status.HTTP_200_OK)
# async def get_leaderboard(db: Session = Depends(get_db)):
#     top_players_by_wins = db.query(User).order_by(User.total_wins.desc()).limit(10).all()
#     top_players_by_points = db.query(User).order_by(User.total_points.desc()).limit(10).all()
#
#     leaderboard_by_wins = [{"username": user.username, "total_wins": user.total_wins} for user in top_players_by_wins]
#     leaderboard_by_points = [{"username": user.username, "total_points": user.total_points} for user in top_players_by_points]
#
#     return {
#         "leaderboard_by_wins": leaderboard_by_wins,
#         "leaderboard_by_points": leaderboard_by_points
#     }
