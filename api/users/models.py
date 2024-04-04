from pydantic import BaseModel


class UserProfileStatistics(BaseModel):
    total_games: int
    total_wins: int
    # total_points: int
    win_percentage: float
    loss_percentage: float
