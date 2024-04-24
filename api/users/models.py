from pydantic import BaseModel


class UserProfileStatistics(BaseModel):
    username: str
    total_games_multiplayer: int
    total_wins_multiplayer: int
    total_points_multiplayer: int
    win_percentage_multiplayer: float
    loss_percentage_multiplayer: float
    total_games_singleplayer: int
    total_wins_singleplayer: int
    total_points_singleplayer: int
    win_percentage_singleplayer: float
    loss_percentage_singleplayer: float

class UpdateUserProfileStats(BaseModel):
    username: str
    total_games_multiplayer: int
    total_wins_multiplayer: int
    total_points_multiplayer: int
    total_games_singleplayer: int
    total_wins_singleplayer: int
    total_points_singleplayer: int
