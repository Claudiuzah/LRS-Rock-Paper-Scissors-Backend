from pydantic import BaseModel
from typing import List


class UpdateUserStats(BaseModel):
    total_wins_multiplayer: int
    total_games_multiplayer: int
    total_points_multiplayer: int
    total_wins_singleplayer: int
    total_games_singleplayer: int
    total_points_singleplayer: int


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




class PlayerMove(BaseModel):
    player_id: str
    choice: str


class GameResult(BaseModel):
    lobby_id: str
    winner_id: str
    player_ids: List[str]
    start_time: str
    end_time: str
    moves: List[PlayerMove]


class UserStatsResponse(BaseModel):
    total_games_singleplayer: int
    total_wins_singleplayer: int
    total_points_singleplayer: int
    total_games_multiplayer: int
    total_wins_multiplayer: int
    total_points_multiplayer: int
