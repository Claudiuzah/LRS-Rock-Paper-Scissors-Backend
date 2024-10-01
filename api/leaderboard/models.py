from pydantic import BaseModel
from typing import List, Dict


class LeaderboardEntry(BaseModel):
    username: str
    total_wins: int = None
    total_points: int = None


class LeaderboardResponse(BaseModel):
    leaderboard_by_wins: List[LeaderboardEntry]
    leaderboard_by_points: List[LeaderboardEntry]
