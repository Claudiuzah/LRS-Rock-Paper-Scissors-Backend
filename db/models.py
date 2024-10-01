from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey, ARRAY, Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker, Session
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
HOSTNAME = os.getenv("HOSTNAME")

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{HOSTNAME}:5432/{DB_NAME}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)


class User_statistics(Base):
    __tablename__ = "user_stats"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    total_games_multiplayer: Mapped[int] = mapped_column(Integer, default=0)
    total_wins_multiplayer: Mapped[int] = mapped_column(Integer, default=0)
    total_points_multiplayer: Mapped[int] = mapped_column(Integer, default=0)
    total_games_singleplayer: Mapped[int] = mapped_column(Integer, default=0)
    total_wins_singleplayer: Mapped[int] = mapped_column(Integer, default=0)
    total_points_singleplayer: Mapped[int] = mapped_column(Integer, default=0)


class Lobby(Base):
    __tablename__ = "lobby"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lobby_name: Mapped[str] = mapped_column(String, unique=True)
    rounds: Mapped[int] = mapped_column(Integer, default=1)


class GameSession(Base):
    __tablename__ = "game_session"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lobby_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lobby.id"))
    winner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    player_ids = Column(ARRAY(String))
    start_time: Mapped[str] = mapped_column(String)
    end_time: Mapped[str] = mapped_column(String)


class Move(Base):
    __tablename__ = "move"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("game_session.id"))
    player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    choice: Mapped[str] = mapped_column(String)


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
