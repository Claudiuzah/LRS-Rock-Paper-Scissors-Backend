import os
from dotenv import load_dotenv

load_dotenv()
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship
from sqlalchemy import ForeignKey, create_engine, ARRAY, Column, Integer

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
HOSTNAME = os.getenv("HOSTNAME")
# from datetime import datetime


import uuid

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{HOSTNAME}:5432/{DB_NAME}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str]
    hashed_password: Mapped[str]

    def __repr__(self):
        return {
            "id": str(self.id),
            "username": str(self.username),
            "password": str(self.hashed_password)
        }


class User_statistics(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    total_games_multiplayer = Column(Integer)
    total_wins_multiplayer = Column(Integer)
    total_points_multiplayer = Column(Integer)
    total_games_singleplayer = Column(Integer)
    total_wins_singleplayer = Column(Integer)
    total_points_singleplayer = Column(Integer)



class Lobby(Base):
    __tablename__ = "lobby"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))  # tb cu relationship
    lobby_name: Mapped[str]
    rounds: Mapped[int]

    def __repr__(self):
        return {
            "id": str(self.id),
            "lobby_name": str(self.lobby_name),
            "rounds": int(self.rounds)
        }


class GameSession(Base):
    __tablename__ = "game_session"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lobby_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lobby.id"))
    winner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    player_ids = Mapped[ARRAY[uuid.UUID]]
    start_time: Mapped[str]
    end_time: Mapped[str]
    player_ids: Mapped[str]

    def __repr__(self):
        return {
            "id": str(self.id),
            "lobby_id": str(self.lobby_id),
            "winner_id": str(self.winner_id),
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "player_ids": str(self.player_ids)
        }


class Move(Base):
    __tablename__ = "move"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("game_session.id"))
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    choice: Mapped[str] = mapped_column()

    def __repr__(self):
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "player_id": str(self.player_id),
            "choice": str(self)
        }


class History(Base):
    __tablename__ = "history"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    opponent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))


class UserLobby(Base):
    __tablename__ = "user_lobby"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    lobby_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lobby.id"))


Base.metadata.create_all(engine)
session = Session(engine)

# TREBUIE RECONFIGURAT DUPA ERD UL NOU
# posibil local cache pentru history
